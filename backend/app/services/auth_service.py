
from app.utils.jwt import create_access_token

from fastapi import HTTPException

from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password, verify_password



class AuthService:

   # Register User 
    def register_user(self, db: Session ,name: str, email:str, password: str):

        hashed_password = hash_password(password)

        new_user = User(
            name = name,
            email = email,
            password = hashed_password
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)


        return {
              "message" : "user registered successfully",
                        "user" : {
                            "id" : new_user.id,
                            "name" : new_user.name,
                            "email" : new_user.email
            }
     
        }



######################################################################################################

    # Login User
    def login_user(self, db: Session, email: str, password: str):

        user = db.query(User).filter(User.email == email).first()
        print("User found:", User is not None)

        if not user:
           raise HTTPException(
               status_code= 401,
               detail= "Invalid email or password"
           )


        if not verify_password(password, user.password):
            raise HTTPException(
                status_code= 401,
                detail= "Invalid email or password"
            )
           

        access_token = create_access_token(
            user_id= user.id,
            email = user.email
        )


        return{
            "message": "Login Successful",
            "user": {
                "id" : user.id,
                "name" : user.name,
                "email" : user.email

            },
            "access_token" : access_token
        }



          
        