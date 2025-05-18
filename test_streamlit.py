import streamlit as st

def main():
    st.title("Simple Streamlit Test")
    st.write("If you can see this, Streamlit is working!")
    
    # Show a simple chart
    import pandas as pd
    import numpy as np
    
    data = pd.DataFrame({
        'x': np.arange(10),
        'y': np.random.randn(10)
    })
    
    st.line_chart(data)

if __name__ == "__main__":
    main()