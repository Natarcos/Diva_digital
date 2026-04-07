# Wrapper para lanzar la app desde la raíz del repositorio
# Permite usar `streamlit run main.py` o configurarlo como entrypoint en el host
import runpy

runpy.run_path('App/diva_digital.py', run_name='__main__')
