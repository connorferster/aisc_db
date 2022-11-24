from aisc_db import load_aisc_db, sections_by_type, values_greater_than, values_less_than, sort_by_weight

def test_load_aisc_db():
    us_df = load_aisc_db('us')
    si_df = load_aisc_db('si')
    assert si_df.iloc[0, 2] == "W1100X499"
    assert us_df.iloc[0, 2] == "W44X335"
    
    
def test_sections_by_type():
    test_df = pd.DataFrame(data = [
        ["X", "A", 200, 300], 
        ["X", "B", 250, 250], 
        ["Y", "C", 400, 600], 
        ["Y", "D", 500, 700]], 
        columns=["Type", "Section", "Ix", "Sy"]
    )
    selection = sections_by_type(test_df, "Y")
    assert selection.iloc[0, 1] == "C"
    assert selection.iloc[1, 1] == "D"
    

def test_values_greater_than():
    test_df = pd.DataFrame(data = [
        ["X", "A", 200, 300], 
        ["X", "B", 250, 250], 
        ["Y", "C", 400, 600], 
        ["Y", "D", 500, 700]], 
        columns=["Type", "Section", "Ix", "Sy"]
    )
    selection = values_greater_than(test_df, Ix=400)
    assert selection.iloc[0, 1] == "C"
    assert selection.iloc[1, 1] == "D"   
    
    
def test_values_less_than():
    test_df = pd.DataFrame(data = [
        ["X", "A", 200, 300], 
        ["X", "B", 250, 250], 
        ["Y", "C", 400, 600], 
        ["Y", "D", 500, 700]], 
        columns=["Type", "Section", "Ix", "Sy"]
    )
    selection = values_less_than(test_df, Sy=300)
    assert selection.iloc[0, 1] == "A"
    assert selection.iloc[1, 1] == "B"   
    
    
def test_sort_by_weight():
    test_df = pd.DataFrame(data = [
        ["X", "A", 200, 300], 
        ["X", "B", 250, 250], 
        ["Y", "C", 400, 600], 
        ["Y", "D", 500, 700]], 
        columns=["Type", "Section", "Ix", "W"]
    )
    selection = sort_by_weight(test_df)
    assert selection.iloc[0, 1] == "B"
    assert selection.iloc[1, 1] == "A"  