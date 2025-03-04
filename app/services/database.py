import os
from supabase import create_client, Client
from dotenv import load_dotenv
from app.models.user import User, ConnectionRequest

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)


async def create_user(user: User) -> User:
    """
    Create a new user in the database.
    
    Args:
        user: User object containing user information
        
    Returns:
        User object with ID
    """
    response = supabase.table("users").insert({
        "name": user.name,
        "phone": user.phone,
        "resume_url": user.resume_url,
        "resume_text": user.resume_text
    }).execute()
    
    data = response.data[0]
    user.id = data.get("id")
    return user


async def get_user(user_id: str) -> User:
    """
    Get a user by ID.
    
    Args:
        user_id: User ID
        
    Returns:
        User object
    """
    response = supabase.table("users").select("*").eq("id", user_id).execute()
    
    if not response.data:
        return None
    
    user_data = response.data[0]
    return User(
        id=user_data.get("id"),
        name=user_data.get("name"),
        phone=user_data.get("phone"),
        resume_url=user_data.get("resume_url"),
        resume_text=user_data.get("resume_text")
    )


async def update_user_resume(user_id: str, resume_url: str, resume_text: str) -> User:
    """
    Update a user's resume.
    
    Args:
        user_id: User ID
        resume_url: URL to the resume file
        resume_text: Extracted text from the resume
        
    Returns:
        Updated User object
    """
    response = supabase.table("users").update({
        "resume_url": resume_url,
        "resume_text": resume_text
    }).eq("id", user_id).execute()
    
    if not response.data:
        return None
    
    user_data = response.data[0]
    return User(
        id=user_data.get("id"),
        name=user_data.get("name"),
        phone=user_data.get("phone"),
        resume_url=user_data.get("resume_url"),
        resume_text=user_data.get("resume_text")
    )


async def get_users_by_category(category: str):
    """
    Get users that match a specific category based on their resume content.
    
    Args:
        category: Category to search for
        
    Returns:
        List of User objects
    """
    # This is a simplified implementation. In a real-world scenario,
    # you might want to use more sophisticated search techniques.
    response = supabase.table("users").select("*").execute()
    
    users = []
    for user_data in response.data:
        resume_text = user_data.get("resume_text", "")
        if resume_text and category.lower() in resume_text.lower():
            users.append(User(
                id=user_data.get("id"),
                name=user_data.get("name"),
                phone=user_data.get("phone"),
                resume_url=user_data.get("resume_url"),
                resume_text=user_data.get("resume_text")
            ))
    
    return users 