import streamlit as st

def main():
    st.title("Text Input Web App")
    
    # Text input
    user_input = st.text_input("Enter some text:", "")
    
    # Display the input
    st.write("You entered:", user_input)

if __name__ == "__main__":
    main()