# -*- coding: utf-8 -*-
import h5py
import os

class HDF5DatasetWriter:
    def __init__(self, outputPath, image_dims, mask_dims, bufSize=200):
        """
        Args:
        - bufSize: 当内存储存了bufSize个数据时，就需要flush到外存
        """
        if os.path.exists(outputPath):
            raise ValueError("The supplied 'outputPath' already"
                             "exists and cannot be overwritten. Manually delete"
                             "the file before continuing", outputPath)
        
        self.db = h5py.File(outputPath, "w")
        # 创建名为images的dataset
        self.data = self.db.create_dataset("images", image_dims, maxshape=(None,)+image_dims[1:], dtype="float32")
        self.masks = self.db.create_dataset("masks", mask_dims, maxshape=(None,)+mask_dims[1:], dtype="float32")
        self.dims = image_dims
        # bufSize 的作用是当内存达到一定程度时，将数据Flush到外存中
        self.bufSize = bufSize
        self.buffer = {"data": [], "masks": []}
        # idx属性表示当前存储的图片数量，最开始为0
        self.idx = 0
    

    def add(self, rows, masks):
        # extend() 函数用于在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表)
        # 注意，用extend还有好处，添加的数据不会是之前list的引用！！
        self.buffer["data"].extend(rows)
        self.buffer["masks"].extend(masks)
#         print("len ",len(self.buffer["data"]))
        
        if len(self.buffer["data"]) >= self.bufSize:
            self.flush()
    
    def flush(self):
        i = self.idx + len(self.buffer["data"])
        if i>self.data.shape[0]:
            # 扩展大小的策略可以自定义，这里乘以2表示直接在原来的基础上扩大一倍
            new_shape = (self.data.shape[0]*2,)+self.dims[1:]
            print("resize to new_shape:",new_shape)
            self.data.resize(new_shape)
            self.masks.resize(new_shape)
        self.data[self.idx:i,:,:,:] = self.buffer["data"]
        self.masks[self.idx:i,:,:,:] = self.buffer["masks"]
        print("h5py have writen %d data"%i)
        self.idx = i
        self.buffer = {"data": [], "masks": []}
        
    
    def close(self):
        if len(self.buffer["data"]) > 0:
            self.flush()
