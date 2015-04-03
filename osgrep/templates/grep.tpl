for f in $(python -c "from __future__ import print_function; import glob; map(lambda f: print(f), glob.glob('{{ path }}'))"); do grep -I -s {{ expression }} $f; done
