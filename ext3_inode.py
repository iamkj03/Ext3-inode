# -*- coding: utf-8 -*-
import sys
import struct
import os
f=open(sys.argv[1],'rb')

f.seek(1024)
sp=f.read(1024)

print("skipping 1024 bytes and reads only the next 1024 bytes from 1024")

#total inode
total_inode = struct.unpack_from("<I", sp, 0x0)[0]
#total block
total_block = struct.unpack_from("<I", sp, 0x4)[0]
#block size
block_size=struct.unpack_from("<I",sp,0x18)[0]
block_size = pow(2, 10+block_size)
#blocks_per_group
blocks_per_group = struct.unpack_from("<I", sp, 0x20)[0]
#inodes_per_group
inodes_per_group = struct.unpack_from("<I", sp, 0x28)[0]
#Inode structure size
inode_structure_size = struct.unpack_from("<H", sp, 0x58)[0]
if(inode_structure_size==4):
    inode_structure_size=256
 
#GDT_entry_size1
gdt_entry_size = struct.unpack_from("<H", sp, 0xFE)[0]
if(gdt_entry_size == 0):
	gdt_entry_size = 32

print("total inode: ", hex(total_inode), total_inode)
print("total block: ", hex(total_block), total_block)
print("block size: ", hex(block_size), block_size)
print("blocks per group: ", hex(blocks_per_group), blocks_per_group)
print("inodes per group: ", hex(inodes_per_group), inodes_per_group)
print("inodes structure size: ", inode_structure_size)
print("gdt_entry_size: ", gdt_entry_size)



if(block_size==pow(2, 10)):
	sp=f.read(32)
	print("Read next 32 from the last whichi is gdt size")

elif(block_size==pow(2, 12)):
	f.seek(4096)
	sp=f.read(32)
	print("Go to 4096 and read only 32 which is gdt size")

#Starting block address of inode table
start_block_inode_table=struct.unpack_from("<I",sp,0x08)[0]
print("starting block inode table: ", hex(start_block_inode_table), start_block_inode_table)

f.seek(block_size*start_block_inode_table+inode_structure_size)
print("From here, go to Block_size(4096) * start_block_inode_table + inode__structure_size = ", 
hex(block_size*start_block_inode_table+inode_structure_size), block_size*start_block_inode_table+inode_structure_size)

#root inode table
print("And then read next 4096 which is a size of ext3 root inode size")
sp=f.read(inode_structure_size)

#file size
file_size=struct.unpack_from("<I",sp,0x4)[0]
print("File size of the file", hex(file_size), file_size)

#block pointer from inode table
block_pointer=struct.unpack_from("<I",sp,0x28)[0]
print("block pointer: ", hex(block_pointer), block_pointer)

#inside the directory(skip . and ..)
f.seek(block_pointer*4096+24+32)
print("directory: ", hex(block_pointer*4096+24+32), block_pointer*4096+24+32)

sp=f.read(32)
record_size=struct.unpack_from("<H",sp,0x4)[0]	
print("record_size: ", hex(record_size), record_size)
direct_inode=struct.unpack_from("<I",sp,0x0)[0]
name_length=struct.unpack_from("<B",sp,0x6)[0]
          
print("direct inode: ", hex(direct_inode), direct_inode)
print("name length: ", hex(name_length), name_length)

f.seek(block_pointer*4096+24+32+8)
directory_name=f.read(name_length)
print("***************************")
print("directory name : ",directory_name)
print("***************************")
               
#block number from gdt  
block_number= (direct_inode/inodes_per_group)                    
                     
#7th gdt          
f.seek(4096+32*6)
sp=f.read(32)

#7th start_inode
block_number_7_start_inode = struct.unpack_from("<I", sp, 0x8)[0]
print("block number 7th starting block address of inode table: ", hex(block_number_7_start_inode), block_number_7_start_inode)
	
#block number 7th inode
f.seek(block_number_7_start_inode*block_size)
sp = f.read(256)

dir2_block_pointer = struct.unpack_from("<I", sp, 0x28)[0]
print("block number 7th starting address: ", hex(block_number_7_start_inode*block_size))
print("dir2's block pointer: ", hex(dir2_block_pointer), dir2_block_pointer)

#directory 2 
f.seek(dir2_block_pointer * block_size + 24)
sp = f.read(256)
print("dir2 entry: ", hex(dir2_block_pointer * block_size), dir2_block_pointer * block_size)
	
#dir2 inode
inode_dir2 = struct.unpack_from("<I", sp, 0x0)[0]
print("dir2's inode: ", hex(inode_dir2), inode_dir2)

#dir2 record length
record_length_dir2 = struct.unpack_from("<H", sp, 0x4)[0]
print("dir2's record length: ", hex(record_length_dir2), record_length_dir2)

#dir2 file length	
file_length_dir2 = struct.unpack_from("<B", sp, 0x6)[0]
print("dir2's file length: ", hex(file_length_dir2), file_length_dir2)
	
#dir2 file type
file_type_dir2 = struct.unpack_from("<B", sp, 0x7)[0]
print("dir2's file type: ", hex(file_type_dir2), file_type_dir2)

#dir2 file name
f.seek(dir2_block_pointer * block_size + 24 + 8)
file_name= f.read(file_length_dir2)
print("dir2 file name: ", file_name)
   


