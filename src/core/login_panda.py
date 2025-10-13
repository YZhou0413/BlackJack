import pandas as pd
import hashlib

USERS_FILENAME = "users.csv"

def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def create_file_check():
    try:
        pd.read_csv(USERS_FILENAME)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["username", "password_hash", "score", "best_score"])
        df.to_csv(USERS_FILENAME, index=False)

def load_df():
    create_file_check()
    df = pd.read_csv(USERS_FILENAME, dtype={"username": str, "password_hash": str})
    return df

def user_exists(username):
    df = load_df()
    return (df['username'].astype(str) == str(username)).any()

def create_user(username, password, start_score):
    username = str(username).strip()
    df = load_df()
    if (df['username'].astype(str) == username).any():
        return False
    row = {
        "username": username,
        "password_hash": hash_password(password),
        "score": int(start_score),
        "best_score": int(start_score)
    }
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(USERS_FILENAME, index = False)
    return True

def verify_user(username, password):
    df = load_df()
    rows = df.loc[df['username'].astype(str) == str(username)]
    return rows.iloc[0]['password_hash'] == hash_password(password)

def get_score(username):
    df = load_df()
    rows = df.loc[df['username'].astype(str) == str(username)]
    val = rows.iloc[0]['score']
    return int(val)

def get_best_core(username):
    df = load_df()
    rows = df.loc[df['username'].astype(str) == str(username)]
    val = rows.iloc[0]['best_score']
    return int(val)

def set_score(username, score):
    df = load_df()
    mask = df['username'].astype(str) == str(username)
    if mask.any():
        df.loc[mask, 'score'] = int(score)

        current_best = df.loc[mask, 'best_score'].iloc[0]
        if int(score) > int(current_best):
            df.loc[mask, 'best_score'] = int(score)

    else:
        df = pd.concat([df, pd.DataFrame([{
            "username": username,
            "password_hash": "",
            "score": int(score),
            "best_score": int(score)
        }])], ignore_index = True)
    df.to_csv(USERS_FILENAME, index = False)

def list_scores(as_df: bool = False):
    df = load_df()
    df['score'] = df['score'].astype(int)
    df['best_score'] = df['best_score'].astype(int)
    if as_df:
        return df[['username', 'score', 'best_score']].copy()
    return dict(zip(df['username'], df['score']))