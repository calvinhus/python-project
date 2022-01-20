import sqlite3

def show_leaders():
    """Show top 3 leaders in escape room game"""
    # Connect to database
    conn = sqlite3.connect('leaderboard.db')
    # Create cursor
    c = conn.cursor()
    c.execute("SELECT * FROM leader LIMIT 3")
    leaders = c.fetchall()
    
    print("\n\n\t---LEADERBOARD---\n\n")
    for l in leaders:
        print(f"User: {l[0]}\tScore: {l[1]}\n")
    
    # Commit the transaction
    conn.commit()
    # Close the connection
    conn.close()



def update_database(lead_list):
    """Update leader table with the winner"""
        # Connect to database
    conn = sqlite3.connect('leaderboard.db')
    # Create cursor
    c = conn.cursor()
    c.execute("INSERT INTO leader VALUES (?,?)",lead_list)
        # Commit the transaction
    conn.commit()
    # Close the connection
    conn.close()


