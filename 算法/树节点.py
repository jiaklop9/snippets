#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
二叉搜索树: 二叉搜索树（Binary Search Tree，BST）是一种有序的二叉树，对于每个节点，其左子树的所有节点值都小于该节点值，右子树的所有节点值都大于该节点值
"""


class TreeNode(object):
    def __init__(self, data):
        self.data = data
        self.left_tree = None
        self.right_tree = None


if __name__ == '__main__':
    root = TreeNode(1)
    root.left_tree = TreeNode(2)
    root.right_tree = TreeNode(3)
    print(root)