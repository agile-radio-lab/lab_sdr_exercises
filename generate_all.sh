SEQ_TYPES=(ones zeros rectangular exp negative_exp cos)

for i in "${SEQ_TYPES[@]}"; do 
python3 seq_gen.py --seq $i --output signals/$i.seq.json
done
