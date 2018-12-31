#!/user/bin/env bash

year() {
    # COLOR
    PLAIN='\033[0m'
    FINISH='\e[1;42m'
    UNDONE='\033[0;47m'
    BARLENGTH=15

    duration=365
    pastdays=$(date +%j)
    YEAR=$(date "+%Y")
    cc="二零一八"
    [ $YEAR = 2019 ] && cc="二零一九"
    
    ratio=$(echo "scale=0; $pastdays * 100 / $duration" | bc )
    int_ration=$((($pastdays  * $BARLENGTH + $duration - 1) / $duration))

    echo -n "#$cc"
    echo "进度条#"
    ##$YEAR  #progress" 

    if [ $(echo "$ratio < 100" | bc) = 1  ]; then 
	if [ $int_ration -lt $BARLENGTH ]; then 			
	    printf "▓%.0s" $(seq 1 $int_ration) 				
	    printf -- "░%.0s" $(seq $((int_ration+=1)) $BARLENGTH)
	else
	    printf "▓%.0s" $(seq 1 $((int_ration-=1))) 				
	    printf -- "░%.0s" $(seq $((int_ration)) $BARLENGTH)
	fi
    else
	printf "▓%.0s" $(seq 1 $int_ration) 				
    fi
    echo -e " $ratio%"
}

while true; do 
    t=$(date +%H)
    if [ $t -eq 22 ]; then 
        year | tee y.dat
        stat=$(cat y.dat)
        python3 p_status.py "$stat"
        rm y.dat
        sleep 2d
    else
        sleep 600
    fi
done
