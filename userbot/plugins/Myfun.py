# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#
#

""" Userbot module for having some fun with people. """

import asyncio
import random
import re
import time

from collections import deque

import requests

from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName

from cowpy import cow

from userbot import CMD_HELP
from userbot.utils import register

# ================= CONSTANT =================
RENDISTR = [
    "`🎶 നാടോടി പൂന്തിങ്കൾ മുടിയിൽ ചൂടി നവരാത്രി പുള്ളോർക്കുടമുള്ളിൽ മീട്ടി കണിക്കൊന്നപ്പൂ മണിക്കമ്മലണിഞ്ഞും പുളിയിലക്കര കസവുമുണ്ടുടുത്തും പുഴയിന്നൊരു നാടൻ പെണ്ണായോ... 🎶`", 
    "`🎶 നീ കണ്ണോട് കണ്ണോട് കണ്ണോരമായ് കാതോട് കാതോട് കാതോരമായ് നെഞ്ചോട് നെഞ്ചോട് നെഞ്ചോരമായ് നിറയേ....🎶`",
    "`🎶 എള്ളോളം തരി പൊന്നെന്തിനാ തനി തഞ്ചാവൂര് പട്ടെന്തിനാ തങ്കം തെളിയണ പട്ടു തിളങ്ങണ ചന്തം നിനക്കാടീ 🎶`", 
    "`🎶 പൂമുത്തോളെ നീയെരിഞ്ഞ വഴിയില്‍ ഞാന്‍മഴയായി പെയ്തെടീ... ആരീരാരം ഇടറല്ലേ മണിമുത്തേ കണ്മണീ... മാറത്തുറക്കാനിന്നോളം തണലെല്ലാം വെയിലായി കൊണ്ടെടീ... മാനത്തോളം മഴവില്ലായ്‌ വളരേണം എന്‍ മണീ ..🎶`", 
    "`🎶 നീ ഹിമമഴയായ് വരൂ... ഹൃദയം അണിവിരലാൽ തൊടൂ... ഈ മിഴിയിണയിൽ സദാ പ്രണയം മഷിയെഴുതുന്നിതാ... ശിലയായി നിന്നിടാം നിന്നെ നോക്കീ യുഗമേറെയെന്റെ കൺചിമ്മിടാതെ... എൻജീവനേ......🎶`", 
    "`🎶 ലല്ലലം ചൊല്ലുന്ന ചെല്ലകിളികളേ വേടന്‍ കുരുക്കും കടങ്കഥ ഇക്കഥ ഇക്കഥയ്ക്കുത്തരം തേടുവാന്‍ കൂടാമോ.. ഇല്ലെങ്കില്‍ സുല്ലെങ്കില്‍ ഇല്ലില്ല സമ്മാനം...🎶`", 
    "`🎶 സുന്ദരീ സുന്ദരീ ഒന്നൊരുങ്ങി വാ നാളെയാണ് താലി മംഗലം.... 🎶`", 
    "`🎶 തൂമിന്നൽ തൂവൽ തുമ്പാൽ മെല്ലെ എൻ പൂവൽ കനവിൽ തഴുകാൻ വരൂ... വാർതിങ്കൾ മായും രാവിൻ കൊമ്പിൽ ചിറകേറി നീ പുലർ വെയിൽ മലർ തരൂ...🎶`", 
    "`🎶 ജീവാംശമായ് താനേ നീ എന്നിൽ കാലങ്ങൾ മുന്നേ വന്നൂ 🎶 `",
    "`🎶 ചന്ദനക്കുറി നീയണിഞ്ഞതിലെന്റെ പേര് പതിഞ്ഞില്ലേ.... 🎶`",
    "`🎶 ആവണിപ്പൊന്നൂഞ്ഞാലാടിക്കാം നിന്നെ ഞാൻ ആയില്യം കാവിലെ വെണ്ണിലാവേ പാതിരാമുല്ലകൾ താലിപ്പൂ ചൂടുമ്പോൾ പൂജിക്കാം നിന്നെ ഞാൻ പൊന്നു പോലെ...🎶`", 
    "`🎶 പണ്ടു പണ്ടേ പൂത്ത മലരുകൾ മിന്നും മിന്നാമിനുങ്ങുകൾ ഒരു കുറി ഇനി വരുമോ...🎶`",
]
NOOBSTR = [
    "`പെമ്പിള്ളേരെ റോട്ടിക്കൂടെ നടക്കാൻ നീ സമ്മതിക്കില്ല , അല്ലേ.......ഡാ, നീയാണീ അലവലാതി ഷാജി അല്ലേ ?`",
    "`വർക്കിച്ചാ യെവൻ പുലിയാണ് കേട്ടാ പുലിയെന്ന് പറഞ്ഞാ വെറും പുലിയല്ല … ഒരു സിംഹം...😜😜 `",
    "`മാമ്മനും അനന്തരവനും കൂടി പണ്ട് ഈഴിര തോർത്തു വെച്ച് പരൽ മീനുകളെ പിടിച്ചു കളിച്ചിട്ടുണ്ടാകും ... പക്ഷെ ആ ഈഴിര വിരിച്ചാൽ സ്രാവിനെ കിട്ടുമെന്നു കരുതരുത് .. ഇത് കാർത്തികേയനാ ...😎😎😎 `",
    "`കഴിഞ്ഞ ഓണത്തിന് കൈപ്പുഴ കുഞ്ഞപ്പന്റെ കയ്യറുത്തപ്പോൾ കട്ടച്ചോരയാ മുഖത്തു തെറിച്ചത് അത്രക്കും വരില്ലല്ലോ ഒരു പീറ ആട്...🤭🤭🤭😜`",
    "`കളി ഹൈറേഞ്ചിലാണെങ്കിലും അങ്ങ് പാരീസിൽ ചെന്ന് ചോദിച്ചാലറിയാം ഈ സാത്താനെ...😎😎😡 `",
    "`എന്റെ ഹൈറേഞ്ചിൽ വന്നിട്ട് എന്റെ പിള്ളേരെ പേടിപ്പിക്കുന്നോടാ നാറികളേ...😡😡😜`",
    "`എവിടെയാടാ നീ അടിച്ചോണ്ട് പോയ എന്റെ നീലക്കുയിൽ 😡😡😜..`",
    "`കൃഷ്ണവിലാസം ഭഗീരഥൻ പിള്ള.. വലിയ വെടി നാല്.. ചെറിയ വെടി നാല്...😜😜🤭`", 
    "`ഇര തേടി വരുന്ന പുലി കെണി തേടി വരില്ല..... പുലിയെ അതിന്റെ മടയിൽ ചെന്ന് വേട്ടയാടി കൊല്ലണം.... അതാണ് കാട്ടിലെ നിയമം...😎😎😇`", 
    "`നീ പോ മോനെ ദിനേശാ...`", "`മരിപ്പിനുള്ള പരിപ്പുവടേം ചായേം ഞാൻ തരുന്നുണ്ട് ഇപ്പോഴല്ല പിന്നെ`", 
    "`സാർ മഹാരാജാസ് കോളേജിൽ പഴേ k.s.u കാരനായിരുന്നല്ലേ അവിടുത്തെ s. F. I പിള്ളേർടെ ഇടി അവസാനത്തേതാണെന്ന് കരുതരുത്...`",
    "`നീയൊക്കെ അര ട്രൗസറും ഇട്ടോണ്ട് അജന്തയിൽ ആദിപാപം കണ്ടോണ്ട് നടക്കണ ടൈമിൽ നമ്മളീ സീൻ വിട്ടതാ നിന്റെയൊക്കെ ഇക്കാനോട് ചോദിച്ചാൽ അറിയാം പോയി ചോദിക്ക് 😎😎😈 `", 
    "`വെല്ലുവിളികൾ ആവാം പക്ഷെ അത് നിന്നെക്കാൾ നാലഞ്ചോണം കൂടുതൽ ഉണ്ടവരോടാവരുത് `", "`ഇവിടെ കിടന്ന് എങ്ങാനും show ഇറക്കാൻ ആണ് പ്ലാൻ എങ്കിൽ പിടിച്ചു തെങ്ങിന്റെ മൂട്ടിലിട്ട് നല്ല വീക്ക് വീക്കും 😡😡😡`", 
    "`ഈ പൂട്ടിന്റെ മുകളിൽ നീ നിന്റെ പൂട്ടിട്ട് പൂട്ടിയാൽ നിന്നെ ഞാൻ പൂട്ടും .. ഒടുക്കത്തെ പൂട്ട് 😡`",
    "`തമ്പുരാൻന്ന് വിളിച്ച അതെ നാവോണ്ട് തന്നെ ചെ** എന്ന് വിളിച്ചതിൽ മനസ്താപണ്ട്..എടോ അപ്പനെന്നു പേരുള്ള തേർഡ് റേറ്റ് ചെ** താനാരാടോ നാട്ടുരാജാവോ 😡😡`", 
    "`ചന്തുവിനെ തോൽപ്പിക്കാൻ ആവില്ല മക്കളേ 😍😍🤗`", 
    "`കൊച്ചി പഴയ കൊച്ചിയെല്ലെന്നറിയാ.... പക്ഷെ ബിലാൽ പഴയ ബിലാൽ തന്നെയാ 😈😈`",
    "`നെട്ടൂരാനോടാണോടാ നിന്റെ കളി 😜😜`", "`ഗോ എവേ സ്റ്റുപ്പിഡ് ഇൻ ദി ഹൗസ് ഓഫ് മൈ വൈഫ്‌ ആൻഡ് ഡോട്ടർ യൂ വിൽ നാട്ട് സീ എനി മിനിറ്റ് ഓഫ് ദി റ്റുഡേ.. എറങ്ങിപ്പോടാ 😜🤭🤣`",
    "`ആണ്ടവൻ ഇത് നിന്റെ കോയമ്പത്തൂരിലെ മായാണ്ടിക്കൊപ്പമല്ല കൊച്ചിയാ വിശ്വനാഥന്റെ കൊച്ചി 😎😎`", 
    "`ഇതെന്റെ പുത്തൻ റെയ്ബാൻ ഗ്ലാസ്സാ ഇത് ചവിട്ടിപൊട്ടിച്ചാ നിന്റെ കാല് ഞാൻ വെട്ടും 😡😡😜`",
]


INSULT_STRINGS = [
     "`Owww ... Such a stupid idiot.`",
    "`Don't drink and type.`",
    "`Command not found. Just like your brain.`",
    "`Bot rule 420 section 69 prevents me from replying to stupid nubfuks like you.`",
    "`Sorry, we do not sell brains.`",
    "`Believe me you are not normal.`",
    "`I bet your brain feels as good as new, seeing that you never use it.`",
    "`If I wanted to kill myself I'd climb your ego and jump to your IQ.`",
    "`You didn't evolve from apes, they evolved from you.`",
    "`What language are you speaking? Cause it sounds like bullshit.`",
    "`You are proof that evolution CAN go in reverse.`",
    "`I would ask you how old you are but I know you can't count that high.`",
    "`As an outsider, what do you think of the human race?`",
    "`If you’re talking behind my back then you’re in a perfect position to kiss my a**!.`",
]

UWUS = [
    "(・`ω´・)",
    ";;w;;",
    "owo",
    "UwU",
    ">w<",
    "^w^",
    r"\(^o\) (/o^)/",
    "( ^ _ ^)∠☆",
    "(ô_ô)",
    "~:o",
    ";-;",
    "(*^*)",
    "(>_",
    "(♥_♥)",
    "*(^O^)*",
    "((+_+))",
]

FACEREACTS = [
    "ʘ‿ʘ",
    "ヾ(-_- )ゞ",
    "(っ˘ڡ˘ς)",
    "(´ж｀ς)",
    "( ಠ ʖ̯ ಠ)",
    "(° ͜ʖ͡°)╭∩╮",
    "(ᵟຶ︵ ᵟຶ)",
    "(งツ)ว",
    "ʚ(•｀",
    "(っ▀¯▀)つ",
    "(◠﹏◠)",
    "( ͡ಠ ʖ̯ ͡ಠ)",
    "( ఠ ͟ʖ ఠ)",
    "(∩｀-´)⊃━☆ﾟ.*･｡ﾟ",
    "(⊃｡•́‿•̀｡)⊃",
    "(._.)",
    "{•̃_•̃}",
    "(ᵔᴥᵔ)",
    "♨_♨",
    "⥀.⥀",
    "ح˚௰˚づ ",
    "(҂◡_◡)",
    "ƪ(ړײ)‎ƪ​​",
    "(っ•́｡•́)♪♬",
    "◖ᵔᴥᵔ◗ ♪ ♫ ",
    "(☞ﾟヮﾟ)☞",
    "[¬º-°]¬",
    "(Ծ‸ Ծ)",
    "(•̀ᴗ•́)و ̑̑",
    "ヾ(´〇`)ﾉ♪♪♪",
    "(ง'̀-'́)ง",
    "ლ(•́•́ლ)",
    "ʕ •́؈•̀ ₎",
    "♪♪ ヽ(ˇ∀ˇ )ゞ",
    "щ（ﾟДﾟщ）",
    "( ˇ෴ˇ )",
    "눈_눈",
    "(๑•́ ₃ •̀๑) ",
    "( ˘ ³˘)♥ ",
    "ԅ(≖‿≖ԅ)",
    "♥‿♥",
    "◔_◔",
    "⁽⁽ଘ( ˊᵕˋ )ଓ⁾⁾",
    "乁( ◔ ౪◔)「      ┑(￣Д ￣)┍",
    "( ఠൠఠ )ﾉ",
    "٩(๏_๏)۶",
    "┌(ㆆ㉨ㆆ)ʃ",
    "ఠ_ఠ",
    "(づ｡◕‿‿◕｡)づ",
    "(ノಠ ∩ಠ)ノ彡( \\o°o)\\",
    "“ヽ(´▽｀)ノ”",
    "༼ ༎ຶ ෴ ༎ຶ༽",
    "｡ﾟ( ﾟஇ‸இﾟ)ﾟ｡",
    "(づ￣ ³￣)づ",
    "(⊙.☉)7",
    "ᕕ( ᐛ )ᕗ",
    "t(-_-t)",
    "(ಥ⌣ಥ)",
    "ヽ༼ ಠ益ಠ ༽ﾉ",
    "༼∵༽ ༼⍨༽ ༼⍢༽ ༼⍤༽",
    "ミ●﹏☉ミ",
    "(⊙_◎)",
    "¿ⓧ_ⓧﮌ",
    "ಠ_ಠ",
    "(´･_･`)",
    "ᕦ(ò_óˇ)ᕤ",
    "⊙﹏⊙",
    "(╯°□°）╯︵ ┻━┻",
    r"¯\_(⊙︿⊙)_/¯",
    "٩◔̯◔۶",
    "°‿‿°",
    "ᕙ(⇀‸↼‶)ᕗ",
    "⊂(◉‿◉)つ",
    "V•ᴥ•V",
    "q(❂‿❂)p",
    "ಥ_ಥ",
    "ฅ^•ﻌ•^ฅ",
    "ಥ﹏ಥ",
    "（ ^_^）o自自o（^_^ ）",
    "ಠ‿ಠ",
    "ヽ(´▽`)/",
    "ᵒᴥᵒ#",
    "( ͡° ͜ʖ ͡°)",
    "┬─┬﻿ ノ( ゜-゜ノ)",
    "ヽ(´ー｀)ノ",
    "☜(⌒▽⌒)☞",
    "ε=ε=ε=┌(;*´Д`)ﾉ",
    "(╬ ಠ益ಠ)",
    "┬─┬⃰͡ (ᵔᵕᵔ͜ )",
    "┻━┻ ︵ヽ(`Д´)ﾉ︵﻿ ┻━┻",
    r"¯\_(ツ)_/¯",
    "ʕᵔᴥᵔʔ",
    "(`･ω･´)",
    "ʕ•ᴥ•ʔ",
    "ლ(｀ー´ლ)",
    "ʕʘ̅͜ʘ̅ʔ",
    "（　ﾟДﾟ）",
    r"¯\(°_o)/¯",
    "(｡◕‿◕｡)",
]

RUNSREACTS = [
    "`Runs to Thanos`",
    "`Runs far, far away from earth`",
    "`Running faster than supercomputer, cuzwhynot`",
    "`Runs to SunnyLeone`",
    "`ZZzzZZzz... Huh? what? oh, just them again, nevermind.`",
    "`Look out for the wall!`",
    "Don't leave me alone with them!!",
    "`You run, you die.`",
    "`Jokes on you, I'm everywhere`",
    "`Running a marathon...there's an app for that.`",
]

RAPE_STRINGS = [
    "`വേലക്കാരി ആയിരുന്താലും നീ എൻ മോഹവല്ലി....🥰`", 
    "`ഭവാനി ഒന്നു മനസ്സ് വെച്ചാൽ ഈ കലവറ നമുക്ക് മണിയറ ആക്കാം.....🥰🥰`", 
    "`ഒരു മുത്തം തരാൻ പാടില്ല എന്നൊന്നും അന്റെ ഉപ്പാപ്പ പറഞ്ഞിട്ടുണ്ടാവില്ലല്ല....🥰😜`", 
    "`ശോഭേ ഞാനൊരു വികാര ജീവിയാണ് 😜😜🥰😂 `",
    "`നിനക്കെന്നെ പ്രേമിച്ചൂടെ കൊച്ചേ 😜😜`",
    "`എങ്കിലേ എന്നോട് പറ ഐ ലവ് യൂന്ന് 🥰🥰🥰 `",
    "`പോരുന്നോ എന്റെ കൂടെ 🥰🥰 `",
    "`എനിക്ക് നിന്റെ പുറകിൽ നടക്കാനല്ല, ഒപ്പം നടക്കാനാണ് ഇഷ്ടം 🥰😍`", 
    "`ഓളാ തട്ടമിട്ടു കഴിഞ്ഞാലെന്റെ സാറേ, പിന്നെ ചുറ്റുമുള്ളതൊന്നും കാണാൻ പറ്റൂല്ലാ 😍🥰`",
] 
ABUSE_STRINGS = [
	   "`Chutiya he rah jaye ga`",
	   "`Ja be Gaandu`",
	   "`Muh Me Lega Bhosdike ?`",
	   "`Kro Gandu giri kam nhi toh Gand Maar lenge tumhari hum😂`",
       "`Suno Lodu Jyda muh na chalo be muh me lawda pel Diyaa jayega`",
       "`Sharam aagyi toh aakhe juka lijia land me dam nhi hai apke toh Shilajit kha lijia`",
       "`Kahe Rahiman Kaviraaj C**t Ki Mahima Aisi,L**d Murjha Jaaye Par Ch**t Waisi Ki Waisi`",
       "`Chudakkad Raand Ki Ch**T Mein Pele L*Nd Kabeer, Par Aisa Bhi Kya Choda Ki Ban Gaye Fakeer`",
]
GEY_STRINGS = [
     "`you gey bsdk`",
     "`you gey`",
     "`you gey in the house`",
     "`you chakka`",
     "`Bhago BC! Chakka aya`",
     "`you gey gey gey gey gey gey gey gey`",
     "`you gey go away`",
]
PRO_STRINGS = [
     "`ഡാ മങ്കി മാങ്ങാതലയാ 😜`", 
     "`വല്യ മലരനാണല്ലോടാ നീ`", 
     "`പോയി ചാവടാ കള്ള പന്നീ`", 
     "`പോയി തൊലയെടാ തവളാച്ചി മോറാ😜 `", 
     "`മാറിപ്പോടാ മരം കൊത്തി മോറാ😜`",
     "`പുന്നാര മോനേ പോയി ചത്തൂടെ നിനക്ക് 😜`",
     "`നീ പോടാ കാട്ടുകോഴീ😜`", 
     "`കോപ്പേ വല്യ ബഹളം വേണ്ട😜`", 
     "`പുന്നാര മോനേ 😜`", 
     "`പ്ഫാ ഇറങ്ങി പോടാ മാക്രി 😜`",
     "`നിന്റെ പെട്ടീം കെടക്കേം എടുത്ത് ഇപ്പോ ഇറങ്ങിക്കോണം ഇവിടുന്ന് `",
     "`ഇനി നീ വാ തുറന്നാൽ മണ്ണ് വാരി ഇടും 😜`",
     "`അടിച്ചു നിന്റെ മണ്ട പൊളിക്കും കേട്ടോടാ മരപ്പട്ടീ... 😡😜`",
     "`മത്തങ്ങാ തലയാ 😜`", 
     "`മാങ്ങാണ്ടി മോറാ 😜`",
]
CHU_STRINGS = [
     "`Taare hai Asmaan me very very bright jaat na jla bskd dekh le apni hight.`",
     "`jindagi ki na toote lari iski lulli hoti nhi khadi`",
     "`Kbhi kbhi meri dil me khyaal ata hai ayse chutiyo ko kon paida kr jata hai😂.`",
     "`Saawan ka mahina pawan kare shor jake gand mara bskd kahi aur.`", 
     "`Dil ke armaa ansuon me beh jaye tum bskd ke chutiye hi reh gye.`",
     "`Ishq Se Tabiyat Ne Zeest Ka Mazaa aya maine is lodu ko randi khane me paya.`",
     "`Mirza galib ki yeh khani hai tu bhosdika hai yeh sab ki jubani hai.`",
]
FUK_STRINGS = [
   "`It's better to let someone think you are an Idiot than to open your mouth and prove it.`",
   "`Talking to a liberal is like trying to explain social media to a 70 years old`",
   "`CHAND PE HAI APUN LAWDE.`",
   "`Pehle main tereko chakna dega, fir daru pilayega, fir jab aap dimag se nahi L*nd se sochoge, tab bolega..`",
   "`Pardhan mantri se number liya, parliament apne :__;baap ka hai...`",
   "`Cachaa Ooo bhosdi wale Chacha`",
   "`Aaisi Londiya Chodiye, L*nd Ka Aapa Khoye, Auro Se Chudi Na Ho, Biwi Wo Hi Hoye`",
   "`Nachoo Bhosdike Nachoo`",
   "`Jinda toh jaat ke baal bhi hai`",
   "`Sab ko pta tu randi ka baccha hai (its just a joke)`", 
]
THANOS_STRINGS = [
   "`തെറി കേട്ടിട്ട് ഇവളുടെ വീട് കൊടുങ്ങല്ലൂർ ഭാഗത്താണെന്ന് തോന്നുന്നു...😜😜`",
   "`പുന്നാര മോളേ😜😜🤭 `", 
   "`ചങ്ക് പറിച്ചു തരുന്ന ചങ്കത്തി കൂടെയുള്ളപ്പോൾ പിന്നെന്തിനാ ലവർ 🥰😜 `",
   "`ഇവൾ നമ്മളേക്കാൾ തറയാടാ...😂😂🤭`",
   "`അഹങ്കാരത്തിന് കയ്യും കാലും വെയ്ക്കാ... എന്നിട്ട് പെണ്ണെന്നു പേരും...🤣🤣😜`",
   "`ആനി മോനെ സ്നേഹിക്കുന്ന പോലെ , മാഗ്ഗിക്ക് എന്നെ സ്നേഹിക്കാമോ...🥰🥰😘`", 
   "`അല്ല ഇതാരാ ! വാര്യംപള്ളിയിലെ മീനാക്ഷിയല്ലയോ ? എന്താ മോളേ സ്കൂട്ടർല്...😜😜🤣`",     
]
ABUSEHARD_STRING = [
     "`നിന്റെ പേരെന്താന്നാ പറഞ്ഞെ -പൈലി ഡ്രാഗൺപൈലി ഡ്യൂഡ് സാറെന്ന്യല്ലേ പേരിട്ടത്.. എന്തൂള പേരാടാത് അയ്യേ...😛😛😜`", 
     "`ദാമോദരൻ ഉണ്ണി മകൻ ദിൽമൻ ഇടക്കൊച്ചി, പീപ്പിൾ കാൾ മീ ഡ്യൂഡ് 😎😎🤨 `", 
     "`മധ്യതിരുവിതാംകൂർ ഭരിച്ച രാജാവാ പേര് ശശി.. 😛😂🤣 `", 
     "`തീരുമ്പോ തീരുമ്പോ പണി തരാൻ ഞാനെന്താ കുപ്പീന്ന് വന്ന ഭൂതോ... 😇😇🙄`",
     "`ഒന്ന് മിണ്ടാതിരിക്കുവോ.. എന്റെ കോൺസെൻട്രേഷൻ പോണ്.. ദേ ആയുധം വെച്ചുള്ള കളിയാ 😝😝😂`", 
     "`സൂക്ഷിച്ചു നോക്കണ്ടടാ ഉണ്ണീ ഇത് ഞാനല്ല...😇🤣🤣`", 
     "`ഈ യന്ത്രങ്ങളുടെ പ്രവർത്തനമൊന്നും താനെന്നെ പഠിപ്പിക്കേണ്ട ഞാനേ പോളിടെക്‌നിക് പഠിച്ചതാ 😎😎😝 `",
     "`ഡിങ്കോൾഫി അല്ലേ ഇത്രക്ക് ചീപ്പാണോ അര്ടിസ്റ്റ് ബേബി😉😉😜 `",
     "`ആദ്യമായി പ്രേമിച്ച പെണ്ണും ആദ്യമായി അടിച്ച ബ്രാൻഡും ഒരാളും ഒരു കാലത്തും മറക്കില്ല്യ😜😜😎`", 
     "`ഡാ മോനേ അത് ലോക്കാ ഇങ്ങ് പോര്.. ഇങ്ങ് പോര്..😇😇🤭`", 
     "`അടിച്ചതാരാടാ നിന്നെ ആണ്ടവനോ സേഡ്‌ജിയോ അടിച്ചതല്ല ചവിട്ടിയതാ ഷൂസിട്ട കാലുകൊണ്ട് 🤭🤭🤭`",
     "`വസൂ... ദേ തോറ്റു തുന്നം പാടി വന്നിരിക്കുന്നു നിന്റെ മോൻ...🤭🤭😜`", 
     "`വോ ലമ്പേ.... വോ ബാത്തേ.... കോഴീ ന ജാനേ.... ങേ കോഴിയോ 🐓🐓🐓`",
     "`എന്താ? പെൺകുട്ടികൾക്കിങ്ങനെ സിമ്പിൾ ഡ്രെസ് ധരിക്കുന്ന പുരുഷന്മാരെ ഇഷ്ടമല്ലേ ? ഡോണ്ട് ദെ ലൈക് ?😎😜`", 
     "`ലേലു അല്ലു ലേലു അല്ലു ലേലു അല്ലു അഴിച്ചു വിട് 🤣🤣`", 
     "`ഇതെന്താ , എനിക്കുമാത്രം പ്രാന്തായതാണോ അതോ നാട്ടുകാർക്ക് മൊത്തത്തിൽ പ്രാന്തായോ ?😇😇🤣`",
     "`അങ്ങനെ പവനായി ശവമായി.. എന്തൊക്കെ ബഹളമായിരുന്നു.. മലപ്പുറം കത്തി, മെഷീൻഗണ്ണു, ബോംബ്, ഒലക്കേടെ മൂട്...🤭🤣🤣`", 
]
HELLOSTR = [
    "`Hi !`",
    "`‘Ello, gov'nor!`",
    "`What’s crackin’?`",
    "`‘Sup, homeslice?`",
    "`Howdy, howdy ,howdy!`",
    "`Hello, who's there, I'm talking.`",
    "`You know who this is.`",
    "`Yo!`",
    "`Whaddup.`",
    "`Greetings and salutations!`",
    "`Hello, sunshine!`",
    "`Hey, howdy, hi!`",
    "`What’s kickin’, little chicken?`",
    "`Peek-a-boo!`",
    "`Howdy-doody!`",
    "`Hey there, freshman!`",
    "`I come in peace!`",
    "`Ahoy, matey!`",
    "`Hiya!`",
    "`Oh retarded gey! Well Hello`",
]

SHGS = [
    "┐(´д｀)┌",
    "┐(´～｀)┌",
    "┐(´ー｀)┌",
    "┐(￣ヘ￣)┌",
    "╮(╯∀╰)╭",
    "╮(╯_╰)╭",
    "┐(´д`)┌",
    "┐(´∀｀)┌",
    "ʅ(́◡◝)ʃ",
    "ლ(ﾟдﾟლ)",
    "┐(ﾟ～ﾟ)┌",
    "┐('д')┌",
    "ლ｜＾Д＾ლ｜",
    "ლ（╹ε╹ლ）",
    "ლ(ಠ益ಠ)ლ",
    "┐(‘～`;)┌",
    "ヘ(´－｀;)ヘ",
    "┐( -“-)┌",
    "乁༼☯‿☯✿༽ㄏ",
    "ʅ（´◔౪◔）ʃ",
    "ლ(•ω •ლ)",
    "ヽ(゜～゜o)ノ",
    "ヽ(~～~ )ノ",
    "┐(~ー~;)┌",
    "┐(-。ー;)┌",
    "¯\_(ツ)_/¯",
    "¯\_(⊙_ʖ⊙)_/¯",
    "乁ʕ •̀ ۝ •́ ʔㄏ",
    "¯\_༼ ಥ ‿ ಥ ༽_/¯",
    "乁( ⁰͡  Ĺ̯ ⁰͡ ) ㄏ",
]

CRI = [
    "أ‿أ",
    "╥﹏╥",
    "(;﹏;)",
    "(ToT)",
    "(┳Д┳)",
    "(ಥ﹏ಥ)",
    "（；へ：）",
    "(T＿T)",
    "（πーπ）",
    "(Ｔ▽Ｔ)",
    "(⋟﹏⋞)",
    "（ｉДｉ）",
    "(´Д⊂ヽ",
    "(;Д;)",
    "（>﹏<）",
    "(TдT)",
    "(つ﹏⊂)",
    "༼☯﹏☯༽",
    "(ノ﹏ヽ)",
    "(ノAヽ)",
    "(╥_╥)",
    "(T⌓T)",
    "(༎ຶ⌑༎ຶ)",
    "(☍﹏⁰)｡",
    "(ಥ_ʖಥ)",
    "(つд⊂)",
    "(≖͞_≖̥)",
    "(இ﹏இ`｡)",
    "༼ಢ_ಢ༽",
    "༼ ༎ຶ ෴ ༎ຶ༽",
]

SLAP_TEMPLATES = [
    "{user1} {victim}ന്റെ തലക്ക് ഒലക്ക കൊണ്ട് അഞ്ചാറു അടി കൊടുത്തു 😪😪 .", 
    "️ {user1} ചാണകം വാരി {victim}ന്റെ മോന്തക്ക് എറിഞ്ഞു 🤢🤮 .",
    "{user1}️  ഓടി വന്ന് {victim}ന്റെ തലയിൽ ചീമുട്ടയെറിഞ്ഞു 🤭🤭😜.",
    "{user1} ️ ️ {victim}നെ കാലേ വാരി നിലത്തടിച്ചു 🤓☹️",
    "{user1}️️ വലിയ പാറക്കല്ലെടുത്തു {victim}ന്റെ തലക്കെറിഞ്ഞു 😱😱🤭 .",
    "{user1}️️ {victim}നെ വിളിച്ചോണ്ട് പോയി പൊട്ടകിണറ്റിൽ തള്ളിയിട്ടു 🤗🤗😝 .", 
    "{user1}️ ️കാക്കയെ വിളിച്ചു വരുത്തി {victim}ന്റെ തലയിൽ അപ്പിയിടീച്ചു 😝🤣 .",
    "{user1} ഓടി വന്ന് ചൂരൽ കൊണ്ട് {victim}ന്റെ ചന്തിക്കിട്ട് അഞ്ചാറു അടി കൊടുത്ത് 😂😜 .",
    "{user1} {victim}നെ കൊതുകിനെ കൊല്ലുന്ന പോലെ അടിച്ചു കൊന്നു 🤭😜.", 
    "{user1}️️ കോഴിക്കാഷ്ടം എടുത്ത് {victim}ന്റെ മുഖത്തു തേച്ചു 🤭🤣.",
    "️ {user1} {victim}ne എടുത്തോണ്ട് പോയി ചാണകക്കുഴിയിലിട്ടു 🤣🤣😛.",
    "{user1}️️ പട്ടിയെ അഴിച്ചു വിട്ട് {victim}ന്റെ ചന്തിയിൽ കടിപ്പിച്ചു 😂😂😛.",
    "{user1}  കട്ടുറുറുമ്പിനെകൊണ്ട് {victim}ന്റെ കുണ്ടിക്ക് കടിപ്പിച്ചു 🤭🤭😜", 
    " {user1} {victim}നെ കോഴിയാണെന്ന് കരുതി കൂട്ടിലടച്ചു 🤭🤭😜", 
]

ITEMS = [
    "cast iron skillet",
    "large trout",
    
]

THROW = [
    "throws",
]

HIT = [
    "hits",
]

# ===========================================


@register(outgoing=True, pattern=r"^.(\w+)say (.*)")
async def univsaye(cowmsg):
    """ For .cowsay module, userbot wrapper for cow which says things. """
    if not cowmsg.text[0].isalpha() and cowmsg.text[0] not in ("/", "#", "@", "!"):
        arg = cowmsg.pattern_match.group(1).lower()
        text = cowmsg.pattern_match.group(2)

        if arg == "cow":
            arg = "default"
        if arg not in cow.COWACTERS:
            return
        cheese = cow.get_cow(arg)
        cheese = cheese()

        await cowmsg.edit(f"`{cheese.milk(text).replace('`', '´')}`")


@register(outgoing=True, pattern="^:/$")
async def kek(keks):
    if not keks.text[0].isalpha() and keks.text[0] not in ("/", "#", "@", "!"):
        """ Check yourself ;)"""
        uio = ["/", "\\"]
        for i in range(1, 15):
            time.sleep(0.3)
            await keks.edit(":" + uio[i % 2])

@register(pattern="^.mslap(?: |$)(.*)", outgoing=True)
async def who(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        """ slaps a user, or get slapped if not a reply. """
        if event.fwd_from:
            return

        replied_user = await get_user(event)
        caption = await slap(replied_user, event)
        message_id_to_reply = event.message.reply_to_msg_id

        if not message_id_to_reply:
            message_id_to_reply = None

        try:
            await event.edit(caption)

        except:
            await event.edit("`Can't slap this person, need to fetch some sticks and stones !!`")

async def get_user(event):
    """ Get the user from argument or replied message. """
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await event.client(GetFullUserRequest(previous_message.from_id))
    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            self_user = await event.client.get_me()
            user = self_user.id

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await event.client.get_entity(user)
            replied_user = await event.client(GetFullUserRequest(user_object.id))

        except (TypeError, ValueError):
            await event.edit("`I don't slap aliens, they ugly AF !!`")
            return None

    return replied_user

async def slap(replied_user, event):
    """ Construct a funny slap sentence !! """
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    username = replied_user.user.username

    if username:
        slapped = "@{}".format(username)
    else:
        slapped = f"[{first_name}](tg://user?id={user_id})"

    temp = random.choice(SLAP_TEMPLATES)
    item = random.choice(ITEMS)
    hit = random.choice(HIT)
    throw = random.choice(THROW)

    caption = "..." + temp.format(victim=slapped, item=item, hits=hit, throws=throw)

    return caption

@register(outgoing=True, pattern="^-_-$")
async def lol(lel):
    if not lel.text[0].isalpha() and lel.text[0] not in ("/", "#", "@", "!"):
        """ Ok... """
        okay = "-_-"
        for _ in range(10):
            okay = okay[:-1] + "_-"
            await lel.edit(okay)

@register(outgoing=True, pattern="^.decide$")
async def _(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        if event.fwd_from:
            return
        message_id = event.message.id
        if event.reply_to_msg_id:
            message_id = event.reply_to_msg_id
        r = requests.get("https://yesno.wtf/api").json()
        await event.client.send_message(
            event.chat_id,
            str(r["answer"]).upper(),
            reply_to=message_id,
            file=r["image"]
        )
        await event.delete()

@register(outgoing=True, pattern="^;_;$")
async def fun(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        t = ";__;"
        for j in range(10):
            t = t[:-1] + "_;"
            await e.edit(t)


@register(outgoing=True, pattern="^.insult$")
async def insult(e):
    """ I make you cry !! """
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit(random.choice(INSULT_STRINGS))


			  
@register(outgoing=True, pattern="^.repo$")
async def source(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("Click [here](https://github.com/sandy1709/catuserbot) to open this lit af repo.")
			  

			  


@register(outgoing=True, pattern="^.hey$")
async def hoi(hello):
    """ Greet everyone! """
    if not hello.text[0].isalpha() and hello.text[0] not in ("/", "#", "@", "!"):
        await hello.edit(random.choice(HELLOSTR))
			  

			  			  
@register(outgoing=True, pattern="^.luv$")
async def raping (raped):
    """ Dont Rape Too much -_-"""
    if not raped.text[0].isalpha() and raped.text[0] not in ("/", "#", "@", "!"):
        index = random.randint(0, len(RAPE_STRINGS) - 1)
        reply_text = RAPE_STRINGS[index]
        await raped.edit(reply_text)
			  
@register(outgoing=True, pattern="^.kil$")
async def proo (pros):
    """ String for Pros only -_-"""
    if not pros.text[0].isalpha() and pros.text[0] not in ("/", "#", "@", "!"):
        index = random.randint(0, len(PRO_STRINGS) - 1)
        reply_text = PRO_STRINGS[index]
        await pros.edit(reply_text)

@register(outgoing=True, pattern="^.fuk$")
async def chutiya (fuks):
    """ String for fhu only -_-"""
    if not fuks.text[0].isalpha() and fuks.text[0] not in ("/", "#", "@", "!"):
        index = random.randint(0, len(CHU_STRINGS) - 1)
        reply_text = FUK_STRINGS[index]
        await fuks.edit(reply_text)

			  			  
@register(outgoing=True, pattern="^.she$")
async def thanos (thanos):
    """ String for thanos only -_-"""
    if not thanos.text[0].isalpha() and thanos.text[0] not in ("/", "#", "@", "!"):
        index = random.randint(0, len(THANOS_STRINGS) - 1)
        reply_text = THANOS_STRINGS[index]
        await thanos.edit(reply_text)	
			  
@register(outgoing=True, pattern="^.fun$")
async def fuckedd (abusehard):
    """ Dont Use this Too much bsdk -_-"""
    if not abusehard.text[0].isalpha() and abusehard.text[0] not in ("/", "#", "@", "!"):
        index = random.randint(0, len(ABUSEHARD_STRING) - 1)
        reply_text = ABUSEHARD_STRING[index]
        await abusehard.edit(reply_text)
			  

			  
			  
@register(outgoing=True, pattern="^.abusehim$")
async def abusing (abused):
    """ Dont Abuse Too much bsdk -_-"""
    if not abused.text[0].isalpha() and abused.text[0] not in ("/", "#", "@", "!"):
        index = random.randint(0, len(ABUSE_STRINGS) - 1)
        reply_text = ABUSE_STRINGS[index]
        await abused.edit(reply_text)


@register(outgoing=True, pattern="^.owo(?: |$)(.*)")
async def faces(owo):
    """ UwU """
    if not owo.text[0].isalpha() and owo.text[0] not in ("/", "#", "@", "!"):
        textx = await owo.get_reply_message()
        message = owo.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await owo.edit("` UwU no text given! `")
            return

        reply_text = re.sub(r"(r|l)", "w", message)
        reply_text = re.sub(r"(R|L)", "W", reply_text)
        reply_text = re.sub(r"n([aeiou])", r"ny\1", reply_text)
        reply_text = re.sub(r"N([aeiouAEIOU])", r"Ny\1", reply_text)
        reply_text = re.sub(r"\!+", " " + random.choice(UWUS), reply_text)
        reply_text = reply_text.replace("ove", "uv")
        reply_text += " " + random.choice(UWUS)
        await owo.edit(reply_text)


@register(outgoing=True, pattern="^.react$")
async def react_meme(react):
    """ Make your userbot react to everything. """
    if not react.text[0].isalpha() and react.text[0] not in ("/", "#", "@", "!"):
        await react.edit(random.choice(FACEREACTS))


@register(outgoing=True, pattern="^.shg$")
async def shrugger(shg):
    r""" ¯\_(ツ)_/¯ """
    if not shg.text[0].isalpha() and shg.text[0] not in ("/", "#", "@", "!"):
        await shg.edit(random.choice(SHGS))


@register(outgoing=True, pattern="^.runs$")
async def runner_lol(run):
    """ Run, run, RUNNN! """
    if not run.text[0].isalpha() and run.text[0] not in ("/", "#", "@", "!"):
        await run.edit(random.choice(RUNSREACTS))

@register(outgoing=True, pattern="^.nom$")
async def metoo(hahayes):
    """ Haha yes """
    if not hahayes.text[0].isalpha() and hahayes.text[0] not in ("/", "#", "@", "!"):
        await hahayes.edit(random.choice(NOOBSTR))
			  
@register(outgoing=True, pattern="^.sing$")
async def metoo(hahayes):
    """ Haha yes """
    if not hahayes.text[0].isalpha() and hahayes.text[0] not in ("/", "#", "@", "!"):
        await hahayes.edit(random.choice(RENDISTR))
			 			  
@register(outgoing=True, pattern="^.oof$")
async def Oof(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        t = "Oof"
        for j in range(15):
            t = t[:-1] + "of"
            await e.edit(t)

@register(outgoing=True, pattern="^.10iq$")
async def iqless(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("♿")

@register(outgoing=True, pattern="^.moon$")
async def _(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
	    if event.fwd_from:
		    return
	    deq = deque(list("🌗🌘🌑🌒🌓🌔🌕🌖"))
	    for _ in range(32):
		    await asyncio.sleep(0.1)
		    await event.edit("".join(deq))
		    deq.rotate(1)

@register(outgoing=True, pattern="^.clock$")
async def _(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
	    if event.fwd_from:
		    return
	    deq = deque(list("🕙🕘🕗🕖🕕🕔🕓🕒🕑🕐🕛"))
	    for _ in range(32):
		    await asyncio.sleep(0.1)
		    await event.edit("".join(deq))
		    deq.rotate(1)


@register(outgoing=True, pattern="^.clap(?: |$)(.*)")
async def claptext(memereview):
    """ Praise people! """
    if not memereview.text[0].isalpha() and memereview.text[0] not in ("/", "#", "@", "!"):
        textx = await memereview.get_reply_message()
        message = memereview.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await memereview.edit("`Hah, I don't clap pointlessly!`")
            return
        reply_text = "👏 "
        reply_text += message.replace(" ", " 👏 ")
        reply_text += " 👏"
        await memereview.edit(reply_text)





@register(outgoing=True, pattern="^.smk (.*)")
async def smrk(smk):
        if not smk.text[0].isalpha() and smk.text[0] not in ("/", "#", "@", "!"):
            textx = await smk.get_reply_message()
            message = smk.text
        if message[5:]:
            message = str(message[5:])
        elif textx:
            message = textx
            message = str(message.message)
        if message == 'dele':
            await smk.edit( message +'te the hell' + "ツ" )
            await smk.edit("ツ")
        else:
             smirk = " ツ"
             reply_text = message + smirk
             await smk.edit(reply_text)


@register(outgoing=True, pattern=r"\.f (.*)")
async def payf(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        paytext = e.pattern_match.group(1)
        pay = "{}\n{}\n{}\n{}\n{}\n{}\n{}".format(paytext*5, paytext*1,paytext*1, paytext*4, paytext*1, paytext*1, paytext*1)
        await e.edit(pay)


@register(outgoing=True, pattern="^.lfy (.*)",)
async def let_me_google_that_for_you(lmgtfy_q):
    if not lmgtfy_q.text[0].isalpha() and lmgtfy_q.text[0] not in ("/", "#", "@", "!"):
        textx = await lmgtfy_q.get_reply_message()
        query = lmgtfy_q.text
        if query[5:]:
            query = str(query[5:])
        elif textx:
            query = textx
            query = query.message
        query_encoded = query.replace(" ", "+")
        lfy_url = f"http://lmgtfy.com/?s=g&iie=1&q={query_encoded}"
        payload = {'format': 'json', 'url': lfy_url}
        r = requests.get('http://is.gd/create.php', params=payload)
        await lmgtfy_q.edit(f"[{query}]({r.json()['shorturl']})")
        if BOTLOG:
            await bot.send_message(
                BOTLOG_CHATID,
                "LMGTFY query `" + query + "` was executed successfully",
            )


			  
@register(pattern='.type(?: |$)(.*)')
async def typewriter(typew):
    """ Just a small command to make your keyboard become a typewriter! """
    if not typew.text[0].isalpha() and typew.text[0] not in ("/", "#", "@", "!"):
        textx = await typew.get_reply_message()
        message = typew.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await typew.edit("`Give a text to type!`")
            return
        sleep_time = 0.03
        typing_symbol = "|"
        old_text = ''
        await typew.edit(typing_symbol)
        await asyncio.sleep(sleep_time)
        for character in message:
            old_text = old_text + "" + character
            typing_text = old_text + "" + typing_symbol
            await typew.edit(typing_text)
            await asyncio.sleep(sleep_time)
            await typew.edit(old_text)
            await asyncio.sleep(sleep_time)

CMD_HELP.update({
    "memes": ".cowsay\
\nUsage: cow which says things.\
\n\n.milksay\
\nUsage: Weird Milk that can speak\
\n\n:/\
\nUsage: Check yourself ;)\
\n\n-_-\
\nUsage: Ok...\
\n\n;_;\
\nUsage: Like `-_-` but crying.\
\n\n.10iq\
\nUsage: You retard !!\
\n\n.oof\
\nUsage: Ooooof\
\n\n.moon\
\nUsage: kensar moon animation.\
\n\n.clock\
\nUsage: kensar clock animation.\
\n\n.earth\
\nUsage: kensar earth animation.\
\n\n.hi\
\nUsage: Greet everyone!\
\n\n.coinflip <heads/tails>\
\nUsage: Flip a coin !!\
\n\n.owo\
\nUsage: UwU\
\n\n.react\
\nUsage: Make your userbot react to everything.\
\n\n.mslap\
\nUsage: reply to slap them with random objects !!\
\n\n.cry\
\nUsage: y u du dis, i cri.\
\n\n.shg\
\nUsage: Shrug at it !!\
\n\n.runs\
\nUsage: Run, run, RUNNN! [`.disable runs`: disable | `.enable runs`: enable]\
\n\n.metoo\
\nUsage: Haha yes\
\n\n.clap\
\nUsage: Praise people!\
\n\n.f <emoji/character>\
\nUsage: Pay Respects.\
\n\n.smk <text/reply>\
\nUsage: A shit module for ツ , who cares.\
\n\n.type\
\nUsage: Just a small command to make your keyboard become a typewriter!\
\n\n.lfy <query>\
\nUsage: Let me Google that for you real quick !!\
\n\n.decide\
\nUsage: Make a quick decision.\
\n\n.fun\
\nUsage: for funny movie dialogues.\
\n\n.chu\
\nUsage: Incase, the person infront of you is....\
\n\n.fuk\
\nUsage: The onlu word that can be used fucking everywhere.\
\n\n.she\
\nUsage: funny theris for females .\
\n\n.nom\
\nUsage: for movie dialogues \
\n\n.kil\
\nUsage: for funny thris hq.\
\n\n.abuse\
\nUsage: Protects you from unwanted peeps.\
"
})
