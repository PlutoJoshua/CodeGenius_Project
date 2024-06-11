import streamlit as st
import psycopg2
import pandas as pd


conn = psycopg2.connect(
    host="localhost", 
    database="django_datamart",
    user="your_username", 
    password="your_password"
)

query = "SELECT * FROM your_table" 
df = pd.read_sql_query(query, conn)