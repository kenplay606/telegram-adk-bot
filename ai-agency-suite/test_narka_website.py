"""
Test script to generate NARKA HK website
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.agents.marketing.website_builder import WebsiteBuilderAgent

async def main():
    print("🚀 Generating NARKA HK Website...")
    print()
    
    # Initialize the website builder for client ID 1 (Narka)
    agent = WebsiteBuilderAgent(client_id=1)
    
    # Build the website
    result = await agent.build_website(
        business_name="NARKA HK (via Simple Feel)",
        business_type="Curated K-Beauty E-Commerce & Brand Showcase",
        description="A high-fidelity digital flagship for NARKA's 'Core Rebuild' philosophy. The site serves as both a high-conversion retail point and an immersive educational portal for the 'Sensorial Hair Care' ritual in the Hong Kong market.",
        features=[
            "Dynamic Dual-Phase UI (Mirrors the product's cream-water split)",
            "Interactive Core-Repair Visualizer",
            "HK-Exclusive Fast-Lane Checkout (PayMe/FPS Integrated)",
            "Scent-Profile Immersive Audio/Visual Backgrounds",
            "AIGC Personal Hair-Type Analysis Tool"
        ]
    )
    
    print("✅ Website generated successfully!")
    print()
    print(f"📁 Files saved to: {result.get('directory', 'N/A')}")
    print()
    print("📄 Generated files:")
    for file_type, content in result.items():
        if file_type not in ['directory', 'metadata']:
            print(f"  - {file_type}: {len(str(content))} characters")
    print()
    print("🌐 HTML Preview (first 500 chars):")
    print("-" * 80)
    print(result.get('html', 'No HTML')[:500])
    print("-" * 80)
    print()
    print("💡 Open the generated HTML file in your browser to view the website!")

if __name__ == "__main__":
    asyncio.run(main())
