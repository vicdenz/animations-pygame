import pygame
import moderngl
import numpy as np
import sys

pygame.init()

# Window setup
WIDTH, HEIGHT = 800, 600

# Mac issue
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
ctx = moderngl.create_context()

# Load texture using Pygame
img = pygame.image.load("python-logo.png").convert_alpha()  # Ensure alpha channel is loaded
img_data = pygame.image.tostring(img, "RGBA", True)
width, height = img.get_size()

# Create texture in ModernGL
texture = ctx.texture((width, height), 4, img_data)
texture.filter = (moderngl.NEAREST, moderngl.NEAREST)  # Set filtering mode
texture.build_mipmaps()  # Build mipmaps

# Calculate aspect ratios
img_aspect = width / height
viewport_aspect = WIDTH / HEIGHT

# Define vertices and texture coordinates for a quad
if img_aspect > viewport_aspect:
    # Image is wider relative to viewport, adjust height
    scale = viewport_aspect / img_aspect
    vertices = np.array([
        # x, y, z, u, v
        -1.0, -scale, 0.0, 0.0, 0.0,  # bottom left
        1.0, -scale, 0.0, 1.0, 0.0,   # bottom right
        1.0, scale, 0.0, 1.0, 1.0,    # top right
        -1.0, scale, 0.0, 0.0, 1.0,   # top left
    ], dtype='f4')
else:
    # Image is taller relative to viewport, adjust width
    scale = img_aspect / viewport_aspect
    vertices = np.array([
        # x, y, z, u, v
        -scale, -1.0, 0.0, 0.0, 0.0,  # bottom left
        scale, -1.0, 0.0, 1.0, 0.0,   # bottom right
        scale, 1.0, 0.0, 1.0, 1.0,    # top right
        -scale, 1.0, 0.0, 0.0, 1.0,   # top left
    ], dtype='f4')

# Create buffer
vbo = ctx.buffer(vertices)

# Define index buffer for drawing the quad
indices = np.array([
    0, 1, 2,  # first triangle
    2, 3, 0,  # second triangle
], dtype='i4')

ibo = ctx.buffer(indices)

# Shaders
vert_shader = '''
#version 330

in vec3 in_vert;
in vec2 in_text;

out vec2 v_text;

void main() {
    gl_Position = vec4(in_vert, 1.0);
    v_text = in_text;
}
'''

frag_shader = '''
#version 330

uniform sampler2D Texture;

in vec2 v_text;
out vec4 f_color;

void main() {
    vec4 color = texture(Texture, v_text);
    f_color = vec4(color.rgb, color.a);  // Ensure alpha is preserved
}
'''

# Create program
program = ctx.program(
    vertex_shader=vert_shader,
    fragment_shader=frag_shader,
)

# Bind attributes
vao = ctx.vertex_array(
    program,
    [
        (vbo, '3f 2f', 'in_vert', 'in_text'),
    ],
    index_buffer=ibo,
)

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ctx.clear(1.0, 1.0, 1.0)
    texture.use()
    vao.render(moderngl.TRIANGLES)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
