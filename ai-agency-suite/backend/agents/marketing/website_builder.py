"""
Website Builder Agent - Creates complete websites for clients
"""
import os
from typing import Dict, Any, Optional
from loguru import logger
from backend.agents.base_agent import BaseAgent


class WebsiteBuilderAgent(BaseAgent):
    """Agent for building complete websites"""
    
    def __init__(self, client_id: int):
        super().__init__(client_id, "WebsiteBuilder")
        self.output_dir = "./websites"
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def build_website(
        self,
        business_name: str,
        business_type: str,
        description: Optional[str] = None,
        features: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Build a complete website
        
        Args:
            business_name: Name of the business
            business_type: Type of business (restaurant, retail, etc.)
            description: Business description
            features: List of features to include
        
        Returns:
            Dictionary with website files and metadata
        """
        logger.info(f"Building website for {business_name}")
        
        # Generate HTML
        html = await self._generate_html(business_name, business_type, description, features)
        
        # Generate CSS
        css = await self._generate_css(business_type)
        
        # Generate JavaScript
        js = await self._generate_js()
        
        # Save files
        site_dir = os.path.join(self.output_dir, business_name.lower().replace(' ', '_'))
        os.makedirs(site_dir, exist_ok=True)
        
        html_path = os.path.join(site_dir, 'index.html')
        css_path = os.path.join(site_dir, 'style.css')
        js_path = os.path.join(site_dir, 'script.js')
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(css)
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(js)
        
        logger.info(f"Website saved to {site_dir}")
        
        return {
            'site_directory': site_dir,
            'html_path': html_path,
            'css_path': css_path,
            'js_path': js_path,
            'business_name': business_name
        }
    
    async def _generate_html(
        self,
        business_name: str,
        business_type: str,
        description: Optional[str],
        features: Optional[list]
    ) -> str:
        """Generate HTML content"""
        prompt = f"""Create a modern, professional HTML5 website for {business_name}, a {business_type} business.

Business Description: {description or 'A professional business'}
Features to include: {', '.join(features) if features else 'hero section, about, services, contact'}

Requirements:
- Modern, responsive design
- Include meta tags for SEO
- Link to style.css and script.js
- Use semantic HTML5 elements
- Include contact form
- Mobile-friendly structure

Generate only the HTML code, no explanations."""
        
        html = await self.generate_with_context(
            prompt=prompt,
            system_prompt="You are an expert web developer. Generate clean, modern HTML5 code.",
            use_memory=False
        )
        
        # Clean up code blocks if present
        if '```html' in html:
            html = html.split('```html')[1].split('```')[0].strip()
        elif '```' in html:
            html = html.split('```')[1].split('```')[0].strip()
        
        return html
    
    async def _generate_css(self, business_type: str) -> str:
        """Generate CSS styles"""
        prompt = f"""Create modern CSS styles for a {business_type} website.

Requirements:
- Modern, clean design
- Responsive layout (mobile-first)
- Professional color scheme appropriate for {business_type}
- Smooth animations
- Flexbox/Grid layout
- Beautiful typography

Generate only the CSS code, no explanations."""
        
        css = await self.generate_with_context(
            prompt=prompt,
            system_prompt="You are an expert CSS developer. Generate clean, modern CSS code.",
            use_memory=False
        )
        
        if '```css' in css:
            css = css.split('```css')[1].split('```')[0].strip()
        elif '```' in css:
            css = css.split('```')[1].split('```')[0].strip()
        
        return css
    
    async def _generate_js(self) -> str:
        """Generate JavaScript functionality"""
        prompt = """Create JavaScript for a modern business website.

Features:
- Smooth scrolling navigation
- Mobile menu toggle
- Form validation
- Scroll animations
- Contact form handling

Generate only the JavaScript code, no explanations."""
        
        js = await self.generate_with_context(
            prompt=prompt,
            system_prompt="You are an expert JavaScript developer. Generate clean, modern ES6+ code.",
            use_memory=False
        )
        
        if '```javascript' in js or '```js' in js:
            js = js.split('```')[1].split('```')[0].strip()
            if js.startswith('javascript') or js.startswith('js'):
                js = '\n'.join(js.split('\n')[1:])
        
        return js
    
    async def optimize_seo(self, html_path: str) -> Dict[str, Any]:
        """Optimize website for SEO"""
        with open(html_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        prompt = f"""Analyze this HTML and suggest SEO improvements:

{html[:2000]}

Provide specific recommendations for:
- Meta tags
- Heading structure
- Image alt text
- Internal linking
- Schema markup

Return as JSON with 'recommendations' array."""
        
        result = await self.generate_json_with_context(
            prompt=prompt,
            system_prompt="You are an SEO expert. Analyze and provide actionable recommendations."
        )
        
        return result
