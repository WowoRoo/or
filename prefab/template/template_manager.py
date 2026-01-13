"""Template manager service."""

from typing import List
from domain.entities.objects_template import ObjectsTemplate


class TemplateManager:
    """Manager for objects templates."""
    
    def __init__(self):
        self.templates: List[ObjectsTemplate] = []
    
    def add_template(self, template: ObjectsTemplate) -> None:
        """Add template to manager."""
        self.templates.append(template)
    
    def get_template(self, template_id) -> ObjectsTemplate:
        """Get template by ID."""
        for template in self.templates:
            if template.id == template_id:
                return template
        raise ValueError(f"Template {template_id} not found")
    
    def get_all_templates(self) -> List[ObjectsTemplate]:
        """Get all templates."""
        return self.templates.copy()

