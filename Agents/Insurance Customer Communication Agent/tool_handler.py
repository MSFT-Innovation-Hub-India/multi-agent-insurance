"""
Tool Handler module for the Insurance Customer Communication Agent

This module handles all tool calls and their execution for the insurance agent.
"""

import json
from typing import Dict, Any, List
from custom_agent_functions import (
    send_insurance_policy_number,
    send_insurance_claim_in_progress, 
    send_insurance_claim_approved,
    send_insurance_claim_rejected
)


class InsuranceToolHandler:
    """Handles all insurance-related tool calls"""
    
    def __init__(self):
        """Initialize the tool handler with available insurance tools"""
        self.available_tools = {
            "send_insurance_policy_number": self._handle_policy_number,
            "send_insurance_claim_in_progress": self._handle_claim_in_progress,
            "send_insurance_claim_approved": self._handle_claim_approved,
            "send_insurance_claim_rejected": self._handle_claim_rejected
        }
    
    def handle_tool_calls(self, tool_calls: List[Any]) -> List[Dict[str, Any]]:
        """
        Handle a list of tool calls and return their outputs
        
        Args:
            tool_calls: List of tool call objects from the agent
            
        Returns:
            List[Dict[str, Any]]: List of tool outputs for the agent
        """
        tool_outputs = []
        
        for tool_call in tool_calls:
            try:
                # Parse the function arguments
                args = json.loads(tool_call.function.arguments)
                tool_name = tool_call.function.name
                
                # Check if the tool is supported
                if tool_name in self.available_tools:
                    print(f"\n📧 Executing insurance tool: {tool_name}")
                    result = self.available_tools[tool_name](args)
                    
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": json.dumps(result)
                    })
                else:
                    # Handle unknown tool calls
                    print(f"\n❌ Unknown tool call: {tool_name}")
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": json.dumps({
                            "error": f"Unknown tool: {tool_name}. Only insurance communication tools are supported."
                        })
                    })
                    
            except Exception as e:
                print(f"Error processing tool call: {str(e)}")
                tool_outputs.append({
                    "tool_call_id": tool_call.id,
                    "output": json.dumps({"error": str(e)})
                })
        
        return tool_outputs
    
    def _handle_policy_number(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle policy number generation tool call"""
        customer_id = args.get("customer_id")
        print(f"Sending policy number generation email for customer {customer_id}...")
        return send_insurance_policy_number(customer_id=customer_id)
    
    def _handle_claim_in_progress(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle claim in progress tool call"""
        customer_id = args.get("customer_id")
        print(f"Sending claim in progress email for customer {customer_id}...")
        return send_insurance_claim_in_progress(customer_id=customer_id)
    
    def _handle_claim_approved(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle claim approved tool call"""
        customer_id = args.get("customer_id")
        print(f"Sending claim approved email for customer {customer_id}...")
        return send_insurance_claim_approved(customer_id=customer_id)
    
    def _handle_claim_rejected(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle claim rejected tool call"""
        customer_id = args.get("customer_id")
        print(f"Sending claim rejected email for customer {customer_id}...")
        return send_insurance_claim_rejected(customer_id=customer_id)
