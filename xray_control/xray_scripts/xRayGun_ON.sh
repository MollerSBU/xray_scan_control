#Check status
#./xray_client_tcp 192.168.1.4 22, 

# Upgraded to accept arguments for kV and mA
#   IF kV argument exists, set the kV
#   IF mA argument exists, set the mA
# otherwise simply turn on with existing parameters

while getopts "k:m:" opt
do
   case "$opt" in
      k ) kV="$OPTARG" ;;
      m ) mA="$OPTARG" ;;
   esac
done

# If the arguments exist, then assert new values:
# Note that these values are integers in the range 0-4095:
#  kV = 4095 is 50 kV
#  mA = 4095 is 5 mA
[ -z "$kV" ] || [ `xray_client_tcp 192.168.1.4 10,$kV,` ] 
[ -z "$mA" ] || [ `xray_client_tcp 192.168.1.4 11,$mA,` ] 

# Begin script in case all parameters are correct
echo "$kV"
echo "$mA"

# Turn high voltage ON
xray_client_tcp 192.168.1.4 99,1,
