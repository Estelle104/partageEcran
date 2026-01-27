import hashlib
import cv2

BLOCK_SIZE = 64

def split_blocks(img):
    h, w, _ = img.shape
    blocks = []
    for y in range(0, h, BLOCK_SIZE):
        for x in range(0, w, BLOCK_SIZE):
            block = img[y:y+BLOCK_SIZE, x:x+BLOCK_SIZE]
            blocks.append(((x, y), block))
    return blocks

def hash_block(block):
    return hashlib.sha1(block.tobytes()).hexdigest()

def diff_blocks(prev_hashes, img):
    changes = []
    blocks = split_blocks(img)

    for idx, ((x, y), block) in enumerate(blocks):
        h = hash_block(block)
        if prev_hashes.get(idx) != h:
            _, encoded = cv2.imencode(".jpg", block, [cv2.IMWRITE_JPEG_QUALITY, 60])
            changes.append((idx, x, y, encoded.tobytes()))
            prev_hashes[idx] = h

    return changes
