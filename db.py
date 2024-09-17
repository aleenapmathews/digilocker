from sqlite3 import connect, IntegrityError


con = connect("drive.db", check_same_thread=False)


cur = con.cursor()

# CREATE TABLE IF NOT EXISTS
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS "hashes" (
	"hash_id"	INTEGER NOT NULL UNIQUE,
	"hash"	TEXT UNIQUE,
	PRIMARY KEY("hash_id" AUTOINCREMENT));     
    """
)
# CREATE TABLE IF NOT EXISTS
cur.execute(
    """
        CREATE TABLE IF NOT EXISTS "users" (
        "username"	TEXT NOT NULL,
        "hash_id"	INTEGER,
        FOREIGN KEY("hash_id") REFERENCES "hashes"("hash_id"));
        """
)
# CREATE TABLE IF NOT EXISTS
cur.execute(
    """
        CREATE TABLE IF NOT EXISTS "files" (
        "id"	INTEGER NOT NULL UNIQUE,
        "file_name"	TEXT NOT NULL,
        "hash_id"	INTEGER,
        PRIMARY KEY("id" AUTOINCREMENT),
        FOREIGN KEY("hash_id") REFERENCES "hashes"("hash_id"));
        """
)


def add_hash_entry(hash):
    try:
        cur.execute(
            f"""
                    INSERT INTO "hashes"(hash) VALUES('{hash}')
                    """
        )
        con.commit()
    except IntegrityError:
        print("hash is not unique")
    except Exception as e:
        print(e)


def add_user_entry(username, hash_id):
    try:
        cur.execute(
            f"""
                    INSERT INTO "users"(username,hash_id)
                    VALUES("{username}","{hash_id}")
                    """
        )
        con.commit()
    except Exception as e:
        print(e)


def add_file_entry(file_name, hash_id):
    try:
        cur.execute(
            f"""
                    INSERT INTO "files" (file_name,hash_id) 
                    VALUES("{file_name}","{hash_id}")
                    
                    """
        )
        con.commit()
    except Exception as e:
        print(e)


def get_hash_id_from_hash(hash):
    try:
        hash_id = cur.execute(
            f"""
                    SELECT "hash_id" from "hashes" where "hash"="{hash}"
                    """
        ).fetchone()[0]

        print(hash_id)
        return hash_id
    except Exception as e:
        print(e)
        return None


def get_hash_from_hash_id(hash_id):
    try:
        hash = cur.execute(
            f"""
                         SELECT "hash" FROM "hashes" where "hash_id"="{hash_id}"
                        """
        ).fetchone()[0]
        print(hash)
        return hash
    except Exception as e:
        print(e)
        return None


def get_username_from_hash_id(hash_id):
    try:
        username = cur.execute(
            f"""
                         SELECT "username" FROM "users" where "hash_id"="{hash_id}"
                        """
        ).fetchone()[0]
        print("1")
        print(username)
        return username
    except Exception as e:
        print(e)
        return None


def get_files_from_hash_id(hash_id):
    try:
        files_temp = cur.execute(
            f"""
                        SELECT "file_name"  FROM "files" WHERE "hash_id"="{hash_id}"  
                        """
        ).fetchall()
        file_names = []
        for i in files_temp:
            file_names.append(i[0])
        print(file_names)
        return file_names
    except Exception as e:
        print(e)
        return None


def delete_file(file_name, hash_id):
    try:
        cur.execute(
            f"""
                    DELETE FROM "files" WHERE "file_name"="{file_name}" AND "hash_id"="{hash_id}"
                    """
        )

        con.commit()
        return True

    except Exception as e:
        print(e)
        return False


# add_file_entry("file1",1)
# get_hash_id_from_hash("1234")
# get_hash_from_hash_id(1)
# get_username_from_hash_id(1)
# get_files_from_hash_id(1)
