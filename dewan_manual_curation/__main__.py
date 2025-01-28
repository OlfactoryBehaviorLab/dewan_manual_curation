import os
os.environ['ISX'] = '0'

from dewan_manual_curation import dewan_manual_curation

if __name__ == '__main__':
    dewan_manual_curation.launch_gui()
