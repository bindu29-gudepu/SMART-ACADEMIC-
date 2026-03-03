# database.py

import sqlite3
import os

DB_PATH = "smart_academic.db"


def connect():
    conn = sqlite3.connect(DB_PATH)
    return conn


def create_tables():
    conn = connect()
    cursor = conn.cursor()

    # Student table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            class INTEGER,
            language TEXT,
            learning_style TEXT,
            study_level TEXT
        )
    """)

    # Scores table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            class INTEGER,
            subject TEXT,
            lesson TEXT,
            score REAL,
            percentage REAL
        )
    """)

    # Leaderboard table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            total_points REAL
        )
    """)

    # Streak table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS streaks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            streak_days INTEGER
        )
    """)

    conn.commit()
    conn.close()


def save_student(name, cls, language, style, level):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO students (name, class, language, learning_style, study_level)
        VALUES (?, ?, ?, ?, ?)
    """, (name, cls, language, style, level))

    conn.commit()
    conn.close()


def save_score(name, cls, subject, lesson, score, percentage):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO scores (student_name, class, subject, lesson, score, percentage)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, cls, subject, lesson, score, percentage))

    conn.commit()
    conn.close()


def update_leaderboard(name, points):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT total_points FROM leaderboard WHERE student_name=?", (name,))
    result = cursor.fetchone()

    if result:
        new_points = result[0] + points
        cursor.execute("UPDATE leaderboard SET total_points=? WHERE student_name=?", (new_points, name))
    else:
        cursor.execute("INSERT INTO leaderboard (student_name, total_points) VALUES (?, ?)", (name, points))

    conn.commit()
    conn.close()


def update_streak(name):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT streak_days FROM streaks WHERE student_name=?", (name,))
    result = cursor.fetchone()

    if result:
        new_streak = result[0] + 1
        cursor.execute("UPDATE streaks SET streak_days=? WHERE student_name=?", (new_streak, name))
    else:
        cursor.execute("INSERT INTO streaks (student_name, streak_days) VALUES (?, ?)", (name, 1))

    conn.commit()
    conn.close()


def get_leaderboard():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT student_name, total_points FROM leaderboard ORDER BY total_points DESC LIMIT 10")
    data = cursor.fetchall()

    conn.close()
    return data
