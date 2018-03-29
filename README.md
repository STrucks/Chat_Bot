## Chat_Bot
Assignment 4 for CCM

------
This project implemens a Chat Bot for Telegram which is able to find a rhyme to a given word and imitate the rappers Kanye West and Eminem. More rappers can be easily added. 

## Greetings, Introduction and Goodbye

The bot will give a welcome message at the beginning of every conversation and tell the user about the !help command. In the command, all other commands are explained.

```
Valentin Koch
Hi
Rap God Chat Bot
Yo, my name is Rap God. Im a Chat Bot.
I am the best, let's give it a test!
You wanna know what I can do, type !help and I can tell you!
Valentin Koch
!help
Rap God Chat Bot
I can immitate rappers. Write somethning and I will rap to that.

!Kanye makes me immitate Kanye West
!Eminem makes me immitate Eminem

If you just want to know a rhyme, type 

 !rhyme *word* and I will give you a rhyme to every word!

Type !Goodbye to let me know you are leaving.
Valentin Koch
!Goodbye
Rap God Chat Bot
Smell ya later, alligator!
```

##Two types of 'domain specific questions'

The bot can do 2 seperate things:

---
He can imitate two different rappers, Kanye West and Eminem. When provided with some text, the bot will rap ongoing from that text.
Switching between rappers is done with !Kanye and !Eminem

---
He can give a rhyme to every word that he is given in combination with the !rhyme command.

#Examples
```
Christopher Strucks
hi
Rap God Chat Bot
Yo, my name is Rap God. Im a Chat Bot.
I am the best, let's give it a test!
You wanna know what I can do, type !help and I can tell you!
Christopher Strucks
!Kanye
Today, I fell off my bike!
Rap God Chat Bot
They smile in my face is what I don't like
They steal your whole sound, that's a soundbite
The media crucify me like they did Christ
They want to find me not breathing like they found Mike
A girl'll run her mouth only out of spite
Valentin Koch
!Eminem
Drop the beat
Rap God Chat Bot
I'm asleep in the front seat
Bumping Heavy D and the Boyz
Still "Chunky, but Funky"
But in my head there's something
I can feel tugging and struggling
Valentin Koch
!rhyme fat rhyme
Rap God Chat Bot
combat coenzyme
```

## Not just querying DB

The bot finds a rhyme by splitting a word into its phonemes and finding words that match as many phonemes as possible, beginning from the last one. Both phonemes as well as the rappers are represented as Databases.
