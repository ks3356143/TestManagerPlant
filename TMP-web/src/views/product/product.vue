<template>
  <div class="app-container">
    <el-table :data="tableData">
      <el-table-column prop="id" label="编号" />
      <el-table-column prop="type" label="类型" />
      <el-table-column prop="keyCode" label="唯一标识" />
      <el-table-column prop="title" label="项目名称" />
      <el-table-column prop="tester" label="测试负责人" />
      <el-table-column prop="seller" label="对接销售" />
      <el-table-column prop="step" label="目前阶段" />
      <el-table-column prop="customer" label="客户名称" />
      <el-table-column prop="begintime" label="开始时间" />
      <el-table-column prop="update" label="操作时间" />
    </el-table>
  </div>
</template>

<script>
import { apiProductList } from "@/api/product";
export default {
  name: "Product",
  data() {
    return {
      tableData: [],
    };
  },
  created() {
    this.getProductList();
  },
  methods: {
    getProductList() {
      apiProductList().then((response) => {
        console.log("获取项目基本信息");
        this.tableData = response.data;
      });
    },
  },
};
</script>

<style></style>
