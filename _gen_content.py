#!/usr/bin/env python3
import json
import time
import urllib.error
import urllib.parse
import urllib.request

REFS = [
    "psalm 16:11", "psalm 18:2", "psalm 18:30", "psalm 19:14", "psalm 20:4",
    "psalm 23:1", "psalm 23:4", "psalm 23:6", "psalm 25:4", "psalm 27:1",
    "psalm 27:13", "psalm 27:14", "psalm 28:7", "psalm 30:5", "psalm 31:24",
    "psalm 32:8", "psalm 33:22", "psalm 34:4", "psalm 34:8", "psalm 34:10",
    "psalm 34:18", "psalm 37:4", "psalm 37:5", "psalm 37:23", "psalm 40:1",
    "psalm 42:11", "psalm 46:1", "psalm 46:5", "psalm 46:10", "psalm 51:12",
    "psalm 55:22", "psalm 56:3", "psalm 61:2", "psalm 62:1", "psalm 63:3",
    "psalm 68:19", "psalm 73:26", "psalm 84:11", "psalm 86:5", "psalm 90:14",
    "psalm 91:1", "psalm 91:4", "psalm 91:11", "psalm 94:19", "psalm 100:5",
    "psalm 103:2", "psalm 103:8", "psalm 103:12", "psalm 107:1", "psalm 112:7",
    "psalm 116:7", "psalm 118:6", "psalm 118:24", "psalm 119:105", "psalm 119:114",
    "psalm 121:1", "psalm 121:2", "psalm 121:7", "psalm 121:8", "psalm 126:3",
    "psalm 133:1", "psalm 136:1", "psalm 138:8", "psalm 139:14", "psalm 143:8",
    "psalm 145:9", "psalm 145:18", "psalm 147:3",
    "proverbs 3:3", "proverbs 3:5", "proverbs 3:6", "proverbs 4:23", "proverbs 11:25",
    "proverbs 12:25", "proverbs 15:13", "proverbs 15:30", "proverbs 16:3",
    "proverbs 16:24", "proverbs 17:17", "proverbs 18:10", "proverbs 27:17",
    "proverbs 31:25",
    "ecclesiastes 4:9", "ecclesiastes 4:10",
    "isaiah 12:2", "isaiah 26:3", "isaiah 30:21", "isaiah 40:11", "isaiah 40:29",
    "isaiah 40:31", "isaiah 41:10", "isaiah 41:13", "isaiah 43:1", "isaiah 43:2",
    "isaiah 43:19", "isaiah 46:4", "isaiah 54:10", "isaiah 58:11",
    "jeremiah 17:7", "jeremiah 29:11", "jeremiah 31:3", "jeremiah 32:17", "jeremiah 33:3",
    "lamentations 3:22", "lamentations 3:23", "lamentations 3:25",
    "micah 6:8", "micah 7:7", "nahum 1:7", "habakkuk 3:19", "zephaniah 3:17",
    "zechariah 4:6",
    "exodus 14:14", "numbers 6:24", "numbers 6:25", "numbers 6:26",
    "deuteronomy 31:6", "deuteronomy 31:8", "joshua 1:9",
    "matthew 5:4", "matthew 5:8", "matthew 5:9", "matthew 5:14", "matthew 5:16",
    "matthew 6:26", "matthew 6:33", "matthew 6:34", "matthew 7:7", "matthew 11:28",
    "matthew 11:29", "matthew 19:26", "matthew 28:20",
    "mark 10:27", "luke 1:37", "luke 6:31", "luke 12:7",
    "john 1:5", "john 3:16", "john 8:12", "john 10:10", "john 13:34",
    "john 14:1", "john 14:27", "john 15:12", "john 15:13", "john 16:33",
    "romans 5:5", "romans 5:8", "romans 8:1", "romans 8:18", "romans 8:28",
    "romans 8:31", "romans 8:38", "romans 8:39", "romans 12:10", "romans 12:12",
    "romans 15:13",
    "1 corinthians 10:13", "1 corinthians 13:4", "1 corinthians 13:7",
    "1 corinthians 15:58", "1 corinthians 16:14",
    "2 corinthians 1:3", "2 corinthians 3:17", "2 corinthians 5:17",
    "2 corinthians 9:8", "2 corinthians 12:9",
    "galatians 5:22", "galatians 6:9",
    "ephesians 2:8", "ephesians 2:10", "ephesians 3:20", "ephesians 4:32", "ephesians 6:10",
    "philippians 1:6", "philippians 4:4", "philippians 4:6", "philippians 4:7",
    "philippians 4:8", "philippians 4:13", "philippians 4:19",
    "colossians 3:12", "colossians 3:15", "colossians 3:23",
    "1 thessalonians 5:11", "1 thessalonians 5:16", "1 thessalonians 5:17",
    "1 thessalonians 5:18",
    "2 thessalonians 2:16", "2 thessalonians 3:3",
    "2 timothy 1:7", "hebrews 4:16", "hebrews 6:19", "hebrews 10:23",
    "hebrews 11:1", "hebrews 12:2", "hebrews 13:5", "hebrews 13:6", "hebrews 13:8",
    "james 1:2", "james 1:5", "james 1:12", "james 1:17", "james 4:8",
    "1 peter 1:3", "1 peter 5:7", "1 peter 5:10",
    "1 john 3:1", "1 john 4:7", "1 john 4:18", "1 john 4:19",
    "revelation 21:4", "revelation 21:5",
]

JOKES = [
    "Why did the birthday cake sit down? It was tiered.",
    "I was going to tell a pencil joke, but it was pointless.",
    "Why don't eggs tell jokes? They would crack each other up.",
    "What do you call a pile of cats? A meow-ntain.",
    "Why did the cookie go to the nurse? It felt crummy.",
    "I know 25 letters of the alphabet. I don't know y.",
    "What do you call cheese that isn't yours? Nacho cheese.",
    "Why did the scarecrow win a prize? He was outstanding in his field.",
    "I used to hate facial hair, but then it grew on me.",
    "What did the ocean say to the shore? Nothing, it just waved.",
    "How do you organize a space party? You planet.",
    "Why did the math book look sad? It had too many problems.",
    "What do you call a bear with no teeth? A gummy bear.",
    "I would tell a construction joke, but I'm still working on it.",
    "Why did the bicycle fall over? It was two tired.",
    "What do you call a fake noodle? An impasta.",
    "Why did the tomato blush? It saw the salad dressing.",
    "I would tell a roof joke, but it might go over your head.",
    "What did one wall say to the other? I'll meet you at the corner.",
    "Why did the golfer bring extra pants? In case he got a hole in one.",
    "How does a penguin build a house? Igloos it together.",
    "What do you call a dinosaur with good teeth? A flossiraptor.",
    "Why did the student eat the homework? The teacher said it was cake.",
    "What did the stamp say to the envelope? Stick with me.",
    "You are the soft color in a loud day.",
    "If hugs were pixels, you would fill the screen.",
    "Why was the broom late? It overswept.",
    "What do you call a sleeping dinosaur? A dino-snore.",
    "Why did the picture go to jail? It was framed.",
    "I asked the suitcase for a joke. It had too much baggage.",
    "What do clouds wear under their coats? Thunderwear.",
    "How do trees get online? They log in.",
    "What do you call a boomerang that won't come back? A stick.",
    "What did the zero say to the eight? Nice belt.",
    "Why did the coffee file a report? It got mugged.",
    "I ordered a chicken and an egg online. I'll let you know which comes first.",
    "Why don't scientists trust atoms? They make up everything.",
    "What do you call a fish with no eyes? A fsh.",
    "How do you make a tissue dance? Put a little boogie in it.",
    "Why was the cookie sad? Its mother had been a wafer too long.",
    "What do you call an alligator in a vest? An investigator.",
    "Why can't a leopard play hide and seek? It is always spotted.",
    "I'm reading a book about anti-gravity. I can't put it down.",
    "Why did the stadium cool off? All the fans left.",
    "What do you call a magic dog? A labracadabrador.",
    "Did you hear about the restaurant on the moon? Great food, no atmosphere.",
    "Why are elevator jokes good? They work on many levels.",
    "You make an ordinary Tuesday feel like confetti.",
    "Why did the leaf go to the doctor? It was feeling green.",
    "What do you call musical whales? An orca-stra.",
    "Why did the banana go to the doctor? It wasn't peeling well.",
    "What did one hat say to the other? You stay here. I'll go on ahead.",
    "Why don't mountains get cold? They wear snow caps.",
    "What is brown and sticky? A stick.",
    "You are proof that gentle people change a room.",
    "A lavender afternoon and your laugh. That is a full plan.",
    "Why did the teddy bear skip dessert? It was stuffed.",
    "What do you call a can opener that doesn't work? A can't opener.",
    "What did the big flower say to the little flower? Hi, bud.",
    "Why was six afraid of seven? Because seven eight nine.",
    "How do you catch a squirrel? Climb a tree and act like a nut.",
    "What do you call a sheep with no legs? A cloud.",
    "Why did the barber win the race? He knew the shortcuts.",
    "What do bees use on their hair? Honeycombs.",
    "What did the blanket say today? I've got you covered.",
    "You are the friend I would pick again on purpose.",
    "Why did the lamp get praised? It was very bright.",
    "What do you call rabbits in a row? A hare-raising event.",
    "What did one raindrop say to the other? Two is company, three is a cloud.",
    "Why was the equal sign humble? It wasn't greater than anyone.",
    "Why don't oysters donate? They are shellfish.",
    "You laugh with your whole face. Please keep that.",
    "How does the moon trim its hair? Eclipse it.",
    "What do you call a bear in the rain? A drizzly bear.",
    "What is a tree's favorite drink? Root beer.",
    "Why are ghosts bad at lying? You can see right through them.",
    "What did the paper say to the pencil? Write on.",
    "You make people feel chosen without a speech.",
    "Why did the clock get in trouble? It was tocking too much.",
    "What do you call a fish in a bow tie? So-fish-ticated.",
    "Why did the baker stop? He was tired of the hole business.",
    "What do you get from a pampered cow? Spoiled milk.",
    "How do you talk to a giant? Use big words.",
    "A small jar and a long friendship work the same way. Keep the good parts.",
    "Why did the phone wear glasses? It lost its contacts.",
    "What do you call a belt made of watches? A waist of time.",
    "What is a witch's favorite class? Spelling.",
    "Why did the melon jump in the lake? It wanted to be a watermelon.",
    "You are easy to celebrate. That is a rare talent.",
    "What do you call a dog at the beach? A hot dog.",
    "What did one eye say to the other? Between us, something smells.",
    "What do you call a funny mountain? Hill-arious.",
    "You saved me a seat in more ways than one.",
    "Why did the grape stop talking? It let out a little whine.",
    "What do you call a cat at the beach? Sandy claws.",
    "Why was the calendar popular? It had too many dates.",
    "How does a dog stop a video? It hits the paws button.",
    "What did the ocean bring to the party? A wave and no speech.",
    "Why did the skeleton stay home? It had nobody to go with.",
    "What do you call a sleeping bull? A bulldozer.",
    "Why don't skeletons fight? They don't have the guts.",
    "You are the kind of kind that sticks.",
    "What is a pirate's favorite letter? You think it is R, but it is the C.",
    "Why did the music note climb? It wanted to be a higher pitch.",
    "What do you call a cow with no legs? Ground beef. Sorry. That one is terrible on purpose.",
    "How do you know a joke is a dad joke? It becomes apparent.",
    "Why did the invisible man decline the job? He couldn't see himself doing it.",
    "What do you call a snowman in July? A puddle.",
    "Why was the broom a good friend? It knew how to sweep the bad day aside.",
    "You turn waiting into a place I don't mind being.",
    "What did the jar say when it was opened? Finally, some air.",
    "Why did the star get a medal? It was a little flashy, in a good way.",
    "What do you call a happy flower? A bloom with a view.",
    "Why did the envelope blush? It knew what the letter said.",
    "A birthday is just a regular day that agreed to wear a party hat for you.",
    "Why don't mountains ever gossip? The echoes would tell.",
    "What do you call a duck that tells jokes? A wise-quacker.",
    "You are the plot twist I am glad happened.",
]

MEMORIES = [
    ("Soft landing", "You are where a loud day goes to get quiet."),
    ("Saved seat", "You keep a place for people, and one of them is me."),
    ("Second cup", "You notice the empty cup before anyone asks."),
    ("Quiet cheer", "You clap for the small wins that nobody else saw."),
    ("Pocket note", "You remember the tiny thing I forgot I said."),
    ("Side by side", "Bad weather is just a reason to stay near."),
    ("Last bite", "You share the good part and never keep score."),
    ("Late lamp", "You stay until the story is actually finished."),
    ("Library voice", "You make a quiet room feel like company."),
    ("Window pointing", "The view gets better when you are the one noticing it."),
    ("Kitchen hum", "An ordinary room turns into a place I want to be."),
    ("Mismatched mugs", "Nothing has to match for it to feel right."),
    ("Silly face", "You never make a face I would refuse to keep."),
    ("Wrong lyrics", "You know the song and still let me sing it wrong."),
    ("No rush", "You find the way without making me hurry."),
    ("Extra blanket", "You notice the cold before I admit it."),
    ("Porch light", "You leave a light on. I can always see it."),
    ("One look", "One look from you and the whole story comes back."),
    ("The good snack", "You remember what I like and act like it was an accident."),
    ("Slow miles", "Distance feels shorter when the talk is good."),
    ("Small handwriting", "You leave courage in little notes."),
    ("Curb picnic", "Any curb becomes a table if you sit down too."),
    ("Warm thing", "You give the warm thing away and pretend it was nothing."),
    ("Morning check", "You make sure I made it to morning."),
    ("This one is you", "You hand me something and say it has my name on it."),
    ("The better wait", "Waiting is the good part when you are in it."),
    ("Room for two", "There is room. With you, there is always room."),
    ("Easy wish", "If today gets one wish, it is that you feel loved."),
    ("Ordinary glass", "You keep beautiful things in plain jars."),
    ("Ground art", "You treat the sidewalk like it asked to be decorated."),
    ("Your songs", "The road feels shorter on your soundtrack."),
    ("The good seat", "You take the cramped spot and call it the view."),
    ("Something warm", "You show up with warmth and no big speech."),
    ("Replay", "You rewind the good part without being asked."),
    ("Your name", "Paper still matters when your name is on it."),
    ("My pace", "You match my steps on the way up."),
    ("Crooked bunch", "You pick the slightly crooked flowers on purpose."),
    ("Laugh that stays", "Your laugh stays in the room after you leave it."),
    ("The call", "You are who I want when a mood locks me out."),
    ("Cloud names", "You name clouds like they introduced themselves."),
    ("Silly yes", "You hold up something ridiculous and I am already nodding."),
    ("Bench hour", "An hour on a bench with you is a complete plan."),
    ("First news", "You are the person I want the first news of the day."),
    ("Future cooking", "You take care of people like you are feeding tomorrow."),
    ("Proof", "You keep the small proof that a day mattered."),
    ("Slow things", "You are patient with slow things, including people."),
    ("Turn to talk", "Wind in our faces, and you still turn toward me."),
    ("Tiny parade", "You cheer a tiny win like it deserves a parade."),
    ("The moon", "When you can't come over, you still send the sky."),
    ("Spare chair", "There is a chair for me in the life you are building."),
    ("Known handwriting", "Your handwriting is a place I recognize."),
    ("Soft reply", "You answer gently when the day was not gentle."),
    ("Arriving", "With you, even a hallway feels like getting home."),
    ("Twenty-two", "This year looks right on you. I am glad I get to see it."),
    ("Still you", "However many years in, I would still pick you first."),
    ("Unfinished sentence", "You let me trail off, and you still understand."),
]


def fetch(ref):
    url = "https://bible-api.com/" + urllib.parse.quote(ref) + "?translation=kjv"
    for attempt in range(8):
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                payload = json.load(response)
            text = " ".join(payload["text"].split())
            time.sleep(0.35)
            return {"ref": payload["reference"], "text": text}
        except urllib.error.HTTPError as error:
            if error.code != 429:
                raise
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(ref)


def main():
    verses = [fetch(ref) for ref in REFS]
    jokes = list(dict.fromkeys(JOKES))
    memories = [
        {"caption": caption, "text": text, "scene": index}
        for index, (caption, text) in enumerate(MEMORIES)
    ]
    if len(verses) <= 100:
        raise SystemExit(f"only {len(verses)} verses")
    if len(jokes) <= 100:
        raise SystemExit(f"only {len(jokes)} jokes")
    if len(memories) <= 50:
        raise SystemExit(f"only {len(memories)} memories")
    birthday = {
        "letter": (
            "Happy birthday.\n\n"
            "I am glad you are in the world today. This note is a placeholder — "
            "write the real one in content.js, in the letter field.\n\n"
            "With love."
        ),
        "verses": verses,
        "jokes": jokes,
        "memories": memories,
    }
    header = """// Edit this file only.
// Photos and videos replace a card when you set src:
// { type: "image", src: "media/photo.jpg", caption: "...", text: "..." }
// { type: "video", src: "media/clip.mp4", caption: "...", text: "..." }
// scene picks the pixel picture when src is left off.
"""
    body = "window.BIRTHDAY = " + json.dumps(birthday, indent=2, ensure_ascii=False) + ";\n"
    with open("content.js", "w", encoding="utf-8") as handle:
        handle.write(header + body)
    print(f"verses {len(verses)} jokes {len(jokes)} memories {len(memories)}")


if __name__ == "__main__":
    main()
