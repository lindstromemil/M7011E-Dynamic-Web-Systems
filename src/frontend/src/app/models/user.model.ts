export interface User {
    "_id": any,
    "created_at": string,
    "password": boolean
    "profile": Profile,
    "username": string,
}

export interface Profile {
    "description": string,
    "image_path": string
}