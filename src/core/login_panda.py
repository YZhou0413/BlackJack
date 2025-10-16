import pandas as pd
import hashlib

USERS_FILENAME = "users.csv"

def hash_password(password):
    # Hash the given password using SHA-256 for secure storage
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def create_file_check():
    # Check if the users.csv file exists; if not, create it with default columns
    try:
        pd.read_csv(USERS_FILENAME)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["username", "password_hash", "score", "best_score"])
        df.to_csv(USERS_FILENAME, index=False)

def load_df():
    # Ensure the CSV file exists, then load and return it as a DataFrame
    create_file_check()
    df = pd.read_csv(USERS_FILENAME, dtype={"username": str, "password_hash": str})
    return df

def user_exists(username):
    # Check if a user with the given username exists in the file
    df = load_df()
    return (df['username'].astype(str) == str(username)).any()

def create_user(username, password, start_score):
    # Create a new user with a hashed password and initial score
    username = str(username).strip()
    df = load_df()
    
    # Prevent duplicate usernames
    if (df['username'].astype(str) == username).any():
        return False

    # Create a new user record
    row = {
        "username": username,
        "password_hash": hash_password(password),
        "score": int(start_score),
        "best_score": int(start_score)
    }

    # Append the new user and save the updated DataFrame
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(USERS_FILENAME, index=False)
    return True

def verify_user(username, password):
    # Verify if the entered password matches the stored hash for a given user
    df = load_df()
    rows = df.loc[df['username'].astype(str) == str(username)]
    return rows.iloc[0]['password_hash'] == hash_password(password)

def get_score(username):
    # Retrieve the current score of a specific user
    df = load_df()
    rows = df.loc[df['username'].astype(str) == str(username)]
    val = rows.iloc[0]['score']
    return int(val)

def get_best_core(username):
    # Retrieve the best (highest) score of a specific user
    df = load_df()
    rows = df.loc[df['username'].astype(str) == str(username)]
    val = rows.iloc[0]['best_score']
    return int(val)

def set_score(username, score):
    # Update the score and best_score for a given user
    df = load_df()
    mask = df['username'].astype(str) == str(username)

    if mask.any():
        # Update existing user's score
        df.loc[mask, 'score'] = int(score)

        # Check if best score needs updating
        current_best = df.loc[mask, 'best_score'].iloc[0]
        if int(score) > int(current_best):
            df.loc[mask, 'best_score'] = int(score)

    else:
        # Create a new record if the user does not exist
        df = pd.concat([df, pd.DataFrame([{
            "username": username,
            "password_hash": "",
            "score": int(score),
            "best_score": int(score)
        }])], ignore_index=True)

    # Save updated data back to the CSV
    df.to_csv(USERS_FILENAME, index=False)

def list_scores(as_df: bool = False):
    # Return all user scores, either as a DataFrame or a dictionary
    df = load_df()
    df['score'] = df['score'].astype(int)
    df['best_score'] = df['best_score'].astype(int)
    
    if as_df:
        # Return DataFrame with selected columns
        return df[['username', 'score', 'best_score']].copy()
    
    # Return dictionary mapping usernames to scores
    return dict(zip(df['username'], df['score']))
