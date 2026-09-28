from backend.database import engine, SessionLocal, Base
from backend.models import AdminUser, Project
from backend.security import get_password_hash
from backend.config import ADMIN_DEFAULT_USERNAME, ADMIN_DEFAULT_PASSWORD

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Check if default admin exists
        admin = db.query(AdminUser).filter(AdminUser.username == ADMIN_DEFAULT_USERNAME).first()
        if not admin:
            admin = AdminUser(
                username=ADMIN_DEFAULT_USERNAME,
                email="admin@reywebstudio.com",
                password_hash=get_password_hash(ADMIN_DEFAULT_PASSWORD),
                is_active=True
            )
            db.add(admin)
            db.commit()
            print(f"[SEED] Initialized Admin User: '{ADMIN_DEFAULT_USERNAME}'")

        # Seed initial projects if empty
        if db.query(Project).count() == 0:
            initial_projects = [
                Project(
                    title="Gym Website",
                    description="Modern responsive gym website with clean UI and fast performance.",
                    image_url="https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b",
                    live_url="https://sample-gym-web.vercel.app/",
                    category="Business Website",
                    featured=True
                ),
                Project(
                    title="AI Business Analytics",
                    description="Modern responsive web page for business analytics.",
                    image_url="https://images.unsplash.com/photo-1460925895917-afdab827c52f",
                    live_url="https://ai-business-analytics-nine.vercel.app/",
                    category="Landing Page",
                    featured=True
                ),
                Project(
                    title="E-commerce UI",
                    description="Simple and clean shopping website interface for online stores.",
                    image_url="https://images.unsplash.com/photo-1556742049-0cfed4f6a45d",
                    live_url=None,
                    category="E-commerce",
                    featured=False
                ),
                Project(
                    title="Portfolio Website",
                    description="Professional portfolio website to showcase projects and skills.",
                    image_url="https://images.unsplash.com/photo-1551288049-bebda4e38f71",
                    live_url="https://fayaz-portfolio-9fh0.onrender.com/",
                    category="Portfolio",
                    featured=True
                )
            ]
            db.add_all(initial_projects)
            db.commit()
            print("[SEED] Initialized 4 default portfolio projects.")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
