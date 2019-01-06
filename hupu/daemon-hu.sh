
{
	nohup python3 -u hupu_bot.py | tee mynohup.out &
} || {
	bash $0 & 
}