import subprocess
from re import sub

import pygame
import pygame_textinput

import d_map
import d_types


def send_to_clipboard():
	subprocess.run(
		" ".join(
			[
				"cat",
				"temp.png",
				"|",
				"xclip",
				"-selection",
				"clipboard",
				"-target",
				"image/png",
				"-i",
			]
		),
		shell=True,
	)
	# win32clipboard.OpenClipboard()
	# win32clipboard.EmptyClipboard()
	# win32clipboard.SetClipboardData(clip_type, data)
	# win32clipboard.CloseClipboard()


WIDTH = 42 * 26 + 2
HEIGHT = 1080 // 2
FPS = 240

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialize pygame and create window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wand Editor")
pygame.display.set_icon(
	pygame.transform.scale(
		pygame.image.load("ui/icon_gun_shuffle.png").convert_alpha(), (7 * 8, 7 * 8)
	)
)
clock = pygame.time.Clock()  # For syncing the FPS

textinput = pygame_textinput.TextInputVisualizer(
	font_color=pygame.Color((255, 255, 255)),
	cursor_color=pygame.Color((255, 255, 255), cursor_width=20),
)

box = pygame.transform.scale(
	pygame.image.load("ui/full_inventory_box.png").convert_alpha(), (40, 40)
)
highlight = pygame.transform.scale(
	pygame.image.load("ui/item_bg_purchase_1.png").convert_alpha(), (40, 40)
)
spell_info = []
translations = d_map.get_info()
enum = [
	"projectile",
	"static_projectile",
	"modifier",
	"draw_many",
	"material",
	"other",
	"utility",
	"passive",
]

for spell in d_types.get_info():
	# print(spell[0][1:])
	try:
		spell_info.append(
			(
				translations[spell[0][1:]],
				enum[spell[1]],
				pygame.transform.scale(
					pygame.image.load(
						"spells/" + spell[2].split("/")[-1]
					).convert_alpha(),
					(32, 32),
				),
				spell[3],
			)
		)
	except KeyError:
		spell_info.append(
			(
				"???",
				enum[spell[1]],
				pygame.transform.scale(
					pygame.image.load(
						"spells/" + spell[2].split("/")[-1]
					).convert_alpha(),
					(32, 32),
				),
				spell[3],
			)
		)
		print(spell[0][1:])


def name_to_id(name):
	for k, v in enumerate(spell_info):
		if v[3] == name:
			return k


# group all the sprites together for ease of update


def tick():
	pass


spells = []
sel = 0


def render_card(x, y, sellected, card=""):
	screen.blit(box, (42 * x + 2, 42 * y + 2))
	if sellected:
		screen.blit(highlight, (42 * x + 2, y + 2))
	if card == "":
		return
	screen.blit(spell_info[card][2], (42 * x + 2 + 4, 42 * y + 2 + 4))


def render():
	x = 0
	y = 2
	for i in range(26):
		# screen.blit(box, (42*i+2, 2))
		# screen.blit(highlight, (42*sel+2, 2))
		try:
			render_card(i, 0, sel == i, name_to_id(spells[i]))
		except:
			render_card(i, 0, sel == i)
		# for k, spell_v in enumerate(spells):
		# screen.blit(spell_info[name_to_id(spell_v)][2], (42*k+2+4, 2+4))

	screen.blit(textinput.surface, (2, 40))
	for k, spell_v in enumerate(spell_info):
		if textinput.value.lower() in spell_v[0].lower():
			render_card(x, y, False, k)
			# screen.blit(box, (x*42+2, y*42+2))
			# screen.blit(spell_info[k][2], (x*42+2+4, y*42+2+4))
			x += 1
			if x >= 26:
				y += 1
				x = 0


# Game loop
running = True
while running:
	clock.tick(FPS)
	events = pygame.event.get()
	dont_input = False

	for event in events:
		# listening for the the X button at the top
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				pos = pygame.mouse.get_pos()
				pos = ((pos[0] - 2) // 42, pos[1] // 42)  # 2 is spell gui, 1
				if pos[1] >= 2:
					try:
						spell = list(
							filter(
								lambda spell: textinput.value.lower()
								in spell[0].lower(),
								spell_info,
							)
						)[(pos[1] - 2) * 26 + pos[0]]
						# print(spell[3])
						if len(spells) < 26:
							spells.insert(sel, spell[3])
							sel += 1
					except IndexError:
						pass
				elif pos[1] == 0:
					try:
						spells.pop(pos[0])
						if pos[0] <= sel:
							sel -= 1
					except IndexError:
						pass
			elif event.button == 5:
				sel += 1
				sel = min(len(spells), sel)
			elif event.button == 4:
				sel -= 1
				sel = max(0, sel)
			# print(pos)
		if event.type == pygame.KEYDOWN:
			if event.unicode == "`":
				dont_input = True
				textinput.value = ""
			try:
				v = int(event.unicode)
				dont_input = True
				if v == 0:
					v = 10
				v -= 1
				try:
					spell = list(
						filter(
							lambda spell: textinput.value.lower() in spell[0].lower(),
							spell_info,
						)
					)[v]
					# print(spell[3])
					if len(spells) < 26:
						spells.insert(sel, spell[3])
						sel += 1
				except IndexError:
					pass
			except ValueError:
				pass
			if event.mod == 64:
				sel -= 1
				sel = max(0, sel)
			elif event.mod == 1:
				sel += 1
				sel = min(len(spells), sel)
			if event.unicode == "\r":
				try:
					spells.pop(sel - 1)
					sel -= 1
				except IndexError:
					pass
			if event.key == 1073742053:
				if len(spells) == 0:
					continue
				rect = pygame.Rect(2, 2, 42 * len(spells), 40)
				scr = pygame.Surface((42 * len(spells), 42))
				scr.blit(screen, area=rect, dest=(0, 0))
				pygame.image.save(scr, "temp.png")
				send_to_clipboard()
			if event.key == 1073742052:
				print(spells)
				ps = subprocess.Popen(
					[
						"luajit",
						"/home/nathan/Documents/code/wand_eval_tree/main.lua",
						"-da",
						"-sc",
						"26",
						"-sp",
					]
					+ [x for x in spells],
					cwd="/home/nathan/Documents/code/wand_eval_tree/",
					stdout=subprocess.PIPE,
				)
				subprocess.Popen(["xclip", "-selection", "clipboard"], stdin=ps.stdout)
				ps.wait()
			if event.unicode == "\\":
				ps = subprocess.Popen(
					["echo", "luajit main.lua -da -sc 26 -sp " + " ".join(spells)],
					stdout=subprocess.PIPE,
				)
				subprocess.Popen(["xclip", "-selection", "clipboard"], stdin=ps.stdout)
				ps.wait()
				dont_input = True
			if event.key == 27:
				exit()

	if not dont_input:
		textinput.update(events)
	else:
		textinput.update([])

	# 3 Draw/render
	screen.fill(BLACK)
	render()
	pygame.display.flip()

pygame.quit()
