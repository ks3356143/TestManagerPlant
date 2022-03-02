<template>
  <div class="app-container">
    <el-dialog
      :title="dialogProductStatus === 'ADD' ? '新增项目' : '修改项目基本信息'"
      :visible.sync="dialogProductShow"
    >
      <el-form :model="product">
        <el-form-item
          v-if="dialogProductStatus === 'UPDATE'"
          label="编号"
          label-width="100px"
        >
          <el-input
            v-model="product.id"
            placeholder="项目顺序编号"
            style="width: 90%"
          ></el-input>
        </el-form-item>
        <el-form-item label="项目类型" label-width="100px">
          <el-input
            v-model="product.type"
            placeholder="请输入项目类型"
            style="width: 90%"
          ></el-input>
        </el-form-item>
        <el-form-item label="项目唯一代号" label-width="100px">
          <el-input
            v-model="product.keyCode"
            placeholder="请输入唯一代号"
            style="width: 90%"
          ></el-input>
        </el-form-item>
        <el-form-item label="项目名称" label-width="100px">
          <el-input
            v-model="product.title"
            placeholder="请输入项目名称"
            style="width: 90%"
          ></el-input>
        </el-form-item>
        <el-form-item label="测试人员" label-width="100px">
          <el-input
            v-model="product.tester"
            placeholder="请输入该项目测试人员"
            style="width: 90%"
          ></el-input>
        </el-form-item>
        <el-form-item label="项目阶段" label-width="100px">
          <el-input
            v-model="product.step"
            placeholder="请输入目前项目阶段"
            style="width: 90%"
          ></el-input>
        </el-form-item>
        <el-form-item label="客户名称" label-width="100px">
          <el-input
            v-model="product.customer"
            placeholder="请输入客户名称"
            style="width: 90%"
          ></el-input>
        </el-form-item>
        <el-form-item label="销售人员" label-width="100px">
          <el-input
            v-model="product.seller"
            placeholder="请输入该项目销售人员"
            style="width: 90%"
          ></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogProductShow = false">取消</el-button>
        <el-button v-if="dialogProductStatus === 'ADD'" type="primary" @click="pCreate()"
          >确定</el-button
        >
        <el-button
          v-if="dialogProductStatus === 'UPDATE'"
          type="primary"
          @click="pUpdate()"
          >修改</el-button
        >
      </span>
    </el-dialog>
    <div class="filter-container">
      <el-form :inline="true" :model="search">
        <el-form-item label="名称">
          <el-input
            v-model="search.title"
            placeholder="支持模糊查询"
            style="width: 200px"
            clearable
          />
        </el-form-item>
        <el-form-item label="项目编号">
          <el-input
            v-model="search.keyCode"
            placeholder="支持模糊查询"
            style="width: 200px"
            clearable
          />
        </el-form-item>
        <el-form-item label="项目编号">
          <el-button type="primary" plain @click="searchProduct()">查询</el-button>
        </el-form-item>
      </el-form>
      <el-button
        type="primary"
        icon="el-icon-plus"
        style="float: right"
        @click="dialogProduct()"
        >新增项目</el-button
      >
    </div>
    <el-table
      :data="tableData"
      border
      :header-cell-style="{ 'text-align': 'center' }"
      :cell-style="{ 'text-align': 'center' }"
    >
      <el-table-column prop="id" label="编号" />
      <el-table-column prop="type" label="项目类型" />
      <el-table-column prop="keyCode" label="唯一标识" />
      <el-table-column prop="title" label="项目名" />
      <el-table-column prop="tester" label="测试负责人" />
      <el-table-column prop="step" label="阶段" />
      <el-table-column prop="customer" label="客户单位" />
      <el-table-column prop="seller" label="销售人员" />
      <el-table-column
        prop="update"
        label="更新时间"
        show-overflow-tooltip=""
        :formatter="formatDate"
      />
      <el-table-column
        prop="begintime"
        label="开始时间"
        show-overflow-tooltip=""
        :formatter="formatDate"
      />
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-link icon="el-icon-edit" @click="dialogProductUpdate(scope.row)"
            >编辑</el-link
          >
          <el-link icon="el-icon-delete" @click="pSoftRemove(scope.row.id)">停用</el-link>
          <el-link icon="el-icon-delete" @click="pHardRemove(scope.row.id)">删除</el-link>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import {
  apiProductList,
  apiProductCreate,
  apiProductUpdate,
  apiProductDelete,
  apiProductRemove,
  apiProductSearch,
} from "@/api/product";
import store from "@/store";
import moment from "moment";
export default {
  name: "Product", // 页面名称
  // data() 数据\属性，固定return中配置
  data() {
    return {
      //定义修改添加状态
      dialogProductStatus: "ADD",
      tableData: [],
      //定义项目添加数据
      op_user: store.getters.name,
      //定义项目参数
      product: {
        id: undefined,
        type: undefined,
        keyCode: undefined,
        title: undefined,
        tester: this.op_user,
        step: undefined,
        customer: undefined,
        seller: undefined,
      },
      //定义控制嵌套表单显示与取消
      dialogProductShow: false,
      //定义模糊搜索数据
      search: {
        title: undefined,
        keyCode: undefined,
      },
    };
  },
  // 页面生命周期中的创建阶段调用
  created() {
    // 调用methods的方法，即初次加载就请求数据
    this.getProductList();
  },
  methods: {
    // getProductList自定义方法名，提供其他地方调用this.getProductList
    getProductList() {
      // 固定格式调用api配置方法，并将返回结果回调给response
      apiProductList().then((response) => {
        // console.log（）是调试打印，可以在chrome开发者工具中查看
        console.log(response.data);
        // 将返回的结果赋值给变量 tableData
        this.tableData = response.data;
      });
    },
    //dialogProduct按钮方法，第一步实现数据情况，然后弹出对话框变量为True
    dialogProduct() {
      //初始化空状态
      (this.product.id = undefined),
        (this.product.type = ""),
        (this.product.keyCode = ""),
        (this.product.title = ""),
        (this.product.tester = ""),
        (this.product.step = ""),
        (this.product.customer = ""),
        (this.product.seller = ""),
        //弹窗变量显示设置为true
        (this.dialogProductShow = true);
      console.log("点击了新增项目按钮");
      //设置dialog为ADD
      this.dialogProductStatus = "ADD";
    },
    pCreate() {
      //实现弹窗添加按钮
      apiProductCreate(this.product).then((response) => {
        this.$notify({
          title: "成功",
          type: "success",
          message: "成功添加项目一个",
        });
        this.getProductList(); //刷新
      });
      //将对话框关闭
      this.dialogProductShow = false;
    },
    dialogProductUpdate(row) {
      //初始化空状态
      (this.product.id = row.id),
        (this.product.type = row.type),
        (this.product.keyCode = row.keyCode),
        (this.product.title = row.title),
        (this.product.tester = row.tester),
        (this.product.step = row.step),
        (this.product.customer = row.customer),
        (this.product.seller = row.seller),
        //弹窗变量显示设置为true
        (this.dialogProductShow = true);
      //标记弹窗为UPDATE
      this.dialogProductStatus = "UPDATE";
      console.log("点击了修改项目信息按钮");
    },
    pUpdate() {
      apiProductUpdate(this.product).then((res) => {
        this.$notify({
          title: "成功",
          message: "项目修改成功",
          type: "success",
        });
        //关闭dialog
        this.dialogProductShow = false;
        //重新查询显示
        this.getProductList();
      });
    },
    pHardRemove(id) {
      this.$confirm("此操作将永久删除项目，请注意", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }).then(() => {
        apiProductDelete(id)
          .then((res) => {
            this.$message({
              type: "success",
              message: "删除成功",
            });
            this.getProductList(); //刷新
          })
          .catch(() => {
            this.$message({
              type: "info",
              message: "已取消删除",
            });
          });
      });
    },
    pSoftRemove(id) {
      this.$confirm("此操作将停用不显示, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          apiProductRemove(id).then((res) => {
            this.$message({
              type: "success",
              message: "删除成功!",
            });
            // 重新查询刷新数据显示
            this.getProductList();
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除",
          });
        });
    },
    searchProduct() {
      apiProductSearch(this.search).then((res) => {
        this.tableData = res.data;
      });
    },
    formatDate(row, column) {
      const date = row[column.property];
      if (date === undefined) {
        return "";
      }
      // 使用moment格式化时间，由于我的数据库是默认时区，偏移量设置0，各自根据情况进行配置
      return moment(date).utcOffset(0).format("YYYY-MM-DD HH:mm");
    },
  },
};
</script>

<style scoped></style>
