
import inspect
import sys

try:
    import euriai.langchain
    print("Successfully imported euriai.langchain")
    
    if hasattr(euriai.langchain, "Field"):
        field_obj = euriai.langchain.Field
        print(f"euriai.langchain.Field: {field_obj}")
        print(f"Type of Field: {type(field_obj)}")
        try:
            print(f"Module of Field: {field_obj.__module__}")
        except:
            pass
    else:
        print("Field not found in euriai.langchain module dict")

    print("\n--- Source Code Top ---")
    try:
        source = inspect.getsource(euriai.langchain)
        for i, line in enumerate(source.splitlines()):
            print(f"{i+1}: {line}")
            if i > 160: break
    except Exception as e:
        print(f"Could not get source: {e}")

except Exception as e:
    print(f"Error importing euriai.langchain: {e}")
