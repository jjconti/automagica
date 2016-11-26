ENV=`python -c "import sys; print sys.prefix"`
PYTHON=`python -c "import sys; print sys.real_prefix"`/bin/python
export PYTHONHOME=$ENV
exec $PYTHON "$@"
