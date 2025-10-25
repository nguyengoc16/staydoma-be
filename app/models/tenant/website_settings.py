import uuid
from sqlalchemy import Column, String, Text, Boolean, JSON, TIMESTAMP, UUID, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import BaseTenant as Base

class WebsiteSettings(Base):
    __tablename__ = "website_settings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True))
    hotel_id = Column(UUID(as_uuid=True), ForeignKey("hotels.id"))
    theme = Column(String)
    logo_url = Column(Text)
    color_scheme = Column(JSON)
    homepage_sections = Column(JSON)
    custom_domain = Column(String)
    is_published = Column(Boolean, default=False)
    updated_at = Column(TIMESTAMP)

    hotel = relationship("Hotels", back_populates="website_settings")
