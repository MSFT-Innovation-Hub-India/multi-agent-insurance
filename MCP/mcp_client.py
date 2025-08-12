import asyncio
import json
import subprocess
import sys
from typing import Dict, Any, Optional, List
import tempfile
import os

class MCPPDFClient:
    def __init__(self, server_path: str):
        self.server_path = server_path
        self.process = None
        self.request_id = 1
        # Default PDF output directory
        self.default_pdf_dir = r"C:\Users\t-ronak\OneDrive - Microsoft\Desktop\MCP\PDF"
        
    def get_pdf_path(self, filename: str) -> str:
        """Get full path for PDF file in the default PDF directory"""
        if not filename.endswith('.pdf'):
            filename += '.pdf'
        return os.path.join(self.default_pdf_dir, filename)
        
    async def start_server(self):
        """Start the MCP server process"""
        try:
            # Change to the pdf-mcp-server directory first
            pdf_server_dir = os.path.join(os.getcwd(), "pdf-mcp-server")
            if os.path.exists(pdf_server_dir):
                os.chdir(pdf_server_dir)
                print(f"✅ Changed to directory: {pdf_server_dir}")
            
            self.process = subprocess.Popen(
                ['node', self.server_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,  # Keep stderr separate
                text=True,
                bufsize=1,  # Line buffered
                cwd=pdf_server_dir if os.path.exists(pdf_server_dir) else None
            )
            
            # Wait a bit for server to start
            await asyncio.sleep(3)
            
            # Check if server started successfully
            if self.process.poll() is not None:
                stderr_output = self.process.stderr.read()
                raise Exception(f"Server failed to start: {stderr_output}")
                
            print("✅ MCP Server started successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            return False
    
    async def send_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send a JSON-RPC request to the MCP server"""
        if not self.process:
            raise Exception("Server not started")
            
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params
        }
        self.request_id += 1
        
        try:
            # Send request
            request_str = json.dumps(request) + '\n'
            self.process.stdin.write(request_str)
            self.process.stdin.flush()
            
            # Read response - may need to skip non-JSON lines
            max_attempts = 10
            for attempt in range(max_attempts):
                response_line = self.process.stdout.readline()
                if not response_line:
                    await asyncio.sleep(0.1)
                    continue
                
                response_line = response_line.strip()
                
                # Skip empty lines and server startup messages
                if not response_line or "MCP server running" in response_line:
                    continue
                
                try:
                    response = json.loads(response_line)
                    
                    if "error" in response:
                        raise Exception(f"Server error: {response['error']}")
                        
                    return response.get("result", {})
                    
                except json.JSONDecodeError:
                    # This might be a partial line or server message, try next line
                    continue
            
            raise Exception("No valid JSON response received after multiple attempts")
            
        except Exception as e:
            raise Exception(f"Request failed: {e}")
    
    def _extract_content_text(self, result: Dict[str, Any]) -> str:
        """Extract text content from MCP server response"""
        if "content" in result and isinstance(result["content"], list):
            for item in result["content"]:
                if item.get("type") == "text":
                    return item.get("text", "")
        return str(result)
    
    def _parse_json_from_text(self, text: str) -> Dict[str, Any]:
        """Try to parse JSON from text response"""
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"raw_text": text}
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """List available tools"""
        result = await self.send_request("tools/list", {})
        return result.get("tools", [])
    
    async def generate_pdf(self, content: str, output_path: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate PDF from markdown content"""
        params = {
            "name": "generate_pdf",
            "arguments": {
                "content": content,
                "output_path": output_path,
                "options": options or {}
            }
        }
        
        result = await self.send_request("tools/call", params)
        text_content = self._extract_content_text(result)
        return self._parse_json_from_text(text_content)
    
    async def embed_images(self, markdown_content: str, image_sources: List[Dict[str, Any]], options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Embed images in markdown content"""
        params = {
            "name": "embed_images",
            "arguments": {
                "markdown_content": markdown_content,
                "image_sources": image_sources,
                "options": options or {}
            }
        }
        
        result = await self.send_request("tools/call", params)
        text_content = self._extract_content_text(result)
        return self._parse_json_from_text(text_content)
    
    async def get_available_themes(self) -> Dict[str, Any]:
        """Get available PDF themes"""
        params = {
            "name": "get_available_themes",
            "arguments": {}
        }
        
        result = await self.send_request("tools/call", params)
        text_content = self._extract_content_text(result)
        return self._parse_json_from_text(text_content)
    
    async def validate_markdown(self, content: str, check_images: bool = False, check_links: bool = False) -> Dict[str, Any]:
        """Validate markdown content"""
        params = {
            "name": "validate_markdown",
            "arguments": {
                "content": content,
                "check_images": check_images,
                "check_links": check_links
            }
        }
        
        result = await self.send_request("tools/call", params)
        text_content = self._extract_content_text(result)
        return self._parse_json_from_text(text_content)
    
    async def create_custom_style(self, style_name: str, description: str = "", prompt: str = "", **kwargs) -> Dict[str, Any]:
        """Create a custom PDF style"""
        params = {
            "name": "create_custom_style",
            "arguments": {
                "style_name": style_name,
                "description": description,
                "prompt": prompt,
                **kwargs
            }
        }
        
        result = await self.send_request("tools/call", params)
        text_content = self._extract_content_text(result)
        return self._parse_json_from_text(text_content)
    
    async def list_custom_styles(self) -> Dict[str, Any]:
        """List all custom styles"""
        params = {
            "name": "list_custom_styles",
            "arguments": {}
        }
        
        result = await self.send_request("tools/call", params)
        text_content = self._extract_content_text(result)
        return self._parse_json_from_text(text_content)
    
    async def generate_pdf_with_style(self, style_name: str, content: str, output_path: str, override_options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate PDF using a custom style"""
        params = {
            "name": "generate_pdf_with_style",
            "arguments": {
                "style_name": style_name,
                "content": content,
                "output_path": output_path,
                "override_options": override_options or {}
            }
        }
        
        result = await self.send_request("tools/call", params)
        text_content = self._extract_content_text(result)
        return self._parse_json_from_text(text_content)
    
    async def get_custom_style(self, style_name: str) -> Dict[str, Any]:
        """Get details of a specific custom style"""
        params = {
            "name": "get_custom_style",
            "arguments": {
                "style_name": style_name
            }
        }
        
        result = await self.send_request("tools/call", params)
        text_content = self._extract_content_text(result)
        return self._parse_json_from_text(text_content)
    
    async def create_styled_template(self, template_name: str, css_content: str, html_template: str = "") -> Dict[str, Any]:
        """Create a reusable styled template"""
        params = {
            "name": "create_styled_template",
            "arguments": {
                "template_name": template_name,
                "css_content": css_content,
                "html_template": html_template
            }
        }
        
        result = await self.send_request("tools/call", params)
        text_content = self._extract_content_text(result)
        return self._parse_json_from_text(text_content)
    
    async def generate_pdf_from_template(self, content: str, template_name: str, output_path: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate PDF using a predefined template"""
        params = {
            "name": "generate_pdf_from_template",
            "arguments": {
                "content": content,
                "template_name": template_name,
                "output_path": output_path,
                "variables": variables or {}
            }
        }
        
        result = await self.send_request("tools/call", params)
        text_content = self._extract_content_text(result)
        return self._parse_json_from_text(text_content)
    
    async def close(self):
        """Close the server process"""
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
            print("✅ Server closed")

# Example usage and test functions
async def example_basic_pdf():
    """Example: Generate a basic PDF"""
    print("📄 Example: Basic PDF Generation")
    
    client = MCPPDFClient("src/index.js")
    
    try:
        await client.start_server()
        
        content = """# Sample Report

## Introduction
This is a professional PDF document generated using the MCP PDF server.

## Features
- **Clean formatting** with professional themes
- *Rich text* support including **bold** and *italic*
- `Code snippets` with proper highlighting
- Lists and structured content

## Technical Specifications
1. Built with Playwright for rendering
2. Markdown-it for content parsing
3. Custom CSS themes available
4. Image embedding support

## Conclusion
The PDF generation is working successfully with all formatting preserved.
"""
        
        # Use the specified PDF output directory
        output_path = client.get_pdf_path("example_basic.pdf")
        
        result = await client.generate_pdf(
            content=content,
            output_path=output_path,
            options={
                "format": "A4",
                "theme": "professional",
                "page_numbers": True,
                "include_toc": True
            }
        )
        
        print(f"✅ PDF generated successfully: {result}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await client.close()

async def example_image_embedding():
    """Example: Embed images in PDF"""
    print("🖼️ Example: PDF with Images")
    
    client = MCPPDFClient("src/index.js")
    
    try:
        await client.start_server()
        
        # First, embed images in markdown
        markdown_content = """# Report with Visualizations

## Overview
This report includes embedded visualizations and charts.

[CHART_1]

The chart above shows our quarterly performance metrics.

## Analysis
Key findings from the data:
- Performance increased by 25%
- Customer satisfaction improved
- Revenue targets exceeded

[DIAGRAM_1]

## Conclusion
The embedded images demonstrate successful integration.
"""
        
        # Using placeholder images for demonstration
        image_sources = [
            {
                "placeholder": "[CHART_1]",
                "source": "https://via.placeholder.com/400x300/4CAF50/FFFFFF?text=Q4+Performance+Chart",
                "alt": "Q4 Performance Chart",
                "caption": "Quarterly Performance Metrics",
                "alignment": "center"
            },
            {
                "placeholder": "[DIAGRAM_1]",
                "source": "https://via.placeholder.com/300x200/2196F3/FFFFFF?text=Process+Diagram",
                "alt": "Process Diagram",
                "caption": "Workflow Process Overview",
                "alignment": "center"
            }
        ]
        
        # Embed images
        embed_result = await client.embed_images(
            markdown_content=markdown_content,
            image_sources=image_sources
        )
        
        print(f"📸 Images embedded: {embed_result.get('embedded_images', 0)}")
        
        # Generate PDF with embedded images
        if "processed_markdown" in embed_result:
            # Use the specified PDF output directory
            output_path = client.get_pdf_path("example_with_images.pdf")
            
            pdf_result = await client.generate_pdf(
                content=embed_result["processed_markdown"],
                output_path=output_path,
                options={
                    "format": "A4",
                    "theme": "default",
                    "page_numbers": True
                }
            )
            
            print(f"✅ PDF with images generated: {pdf_result}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await client.close()

async def example_custom_style():
    """Example: Create and use custom styles"""
    print("🎨 Example: Custom Style PDF")
    
    client = MCPPDFClient("src/index.js")
    
    try:
        await client.start_server()
        
        # Create a custom style
        style_result = await client.create_custom_style(
            style_name="corporate_report",
            description="Corporate report style with branded formatting",
            prompt="Create a professional corporate document with executive summary formatting",
            theme="professional",
            format="A4",
            page_numbers=True,
            include_toc=True,
            custom_css="""
            .executive-summary {
                background-color: #f8f9fa;
                border-left: 4px solid #007bff;
                padding: 1rem;
                margin: 1rem 0;
            }
            """,
            header="<div style='text-align: right; font-size: 12px; color: #666;'>Corporate Report 2025</div>",
            footer="<div style='text-align: center; font-size: 10px; color: #666;'>Confidential - Page {pageNumber}</div>"
        )
        
        print(f"🎨 Custom style created: {style_result}")
        
        # Use the custom style
        content = """# Executive Summary

<div class="executive-summary">
This quarterly report presents our key performance indicators and strategic initiatives for Q4 2025.
</div>

## Financial Performance
Our revenue increased by 23% compared to the previous quarter, driven by:
- Strong product sales
- Improved customer retention
- Successful market expansion

## Strategic Initiatives
- Digital transformation projects
- Sustainability program launch
- Team expansion in key markets

## Looking Forward
The outlook for 2026 remains positive with continued growth expected.
"""
        
        # Use the specified PDF output directory
        output_path = client.get_pdf_path("example_corporate.pdf")
        
        pdf_result = await client.generate_pdf_with_style(
            style_name="corporate_report",
            content=content,
            output_path=output_path
        )
        
        print(f"✅ Corporate PDF generated: {pdf_result}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await client.close()

async def main():
    """Run all examples"""
    print("🚀 PDF MCP Client - Working Examples\n")
    
    # Ensure we're in the right directory
    original_dir = os.getcwd()
    
    try:
        await example_basic_pdf()
        print("\n" + "="*60 + "\n")
        
        await example_image_embedding()
        print("\n" + "="*60 + "\n")
        
        await example_custom_style()
        
        print("\n🎉 All examples completed successfully!")
        print("\nGenerated files:")
        pdf_dir = r"C:\Users\t-ronak\OneDrive - Microsoft\Desktop\MCP\PDF"
        for filename in ["example_basic.pdf", "example_with_images.pdf", "example_corporate.pdf"]:
            filepath = os.path.join(pdf_dir, filename)
            if os.path.exists(filepath):
                size = os.path.getsize(filepath)
                print(f"  - {filename} ({size} bytes) -> {filepath}")
        
    except Exception as e:
        print(f"❌ Examples failed: {e}")
    finally:
        # Restore original directory
        os.chdir(original_dir)

if __name__ == "__main__":
    asyncio.run(main())