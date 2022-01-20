import sqlite3

# Connect to database
conn = sqlite3.connect('leaderboard.db')

# Create cursor
c = conn.cursor()

# Create table
c.execute("CREATE TABLE leader (USER text, TIME real)")

# Commit the transaction
conn.commit()

# Close the connection
conn.close()