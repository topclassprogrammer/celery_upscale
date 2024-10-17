while true
do
  pytest . -s -v -W ignore::DeprecationWarning
  sleep 86400
done

