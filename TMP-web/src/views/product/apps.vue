<template>
  <div class="app-container">
    <el-drawer
      :title="appAction === 'ADD' ? '添加' : '修改'"
      :visible.sync="drawerVisible"
      size="45%"
      direction="rtl"
    >
      <div>
        <el-form :model="appInfo" :rules="rules" ref="appInfo" label-width="120px">
          <el-form-item label="测试名称" prop="name">
            <el-input
              v-model="appInfo.name"
              :disabled="appAction === 'ADD' ? false : true"
              style="width: 300px"
            />
          </el-form-item>
          <el-form-item label="归属分类" prop="productId">
            <el-select v-model="appInfo.productId" style="width: 300px">
              <el-option
                v-for="item in options"
                :key="item.id"
                :label="item.title"
                :value="item.id"
              >
                <span style="float: left">{{ item.keyCode }}</span>
                <span style="float: right; color: #8492a6; font-size: 13px">{{
                  item.title
                }}</span>
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="应用描述">
            <el-input v-model="appInfo.note" style="width: 300px" />
          </el-form-item>
          <el-form-item label="测试级别" prop="level">
            <el-input v-model="appInfo.level" style="width: 300px" />
          </el-form-item>
          <el-form-item label="‘新研’/‘改造’" prop="junstatus">
            <el-input v-model="appInfo.junstatus" style="width: 300px" />
          </el-form-item>
          <el-form-item label="输入负责人" prop="producer">
            <el-input v-model="appInfo.producer" style="width: 300px" />
          </el-form-item>
          <el-form-item label="请输入创建人">
            <el-input v-model="appInfo.creteUser" style="width: 300px" />
          </el-form-item>
          <el-form-item label="请输入更新人">
            <el-input v-model="appInfo.updateUser" style="width: 300px" />
          </el-form-item>
          <el-form-item>
            <span class="dialog-footer">
              <el-button @click="drawerVisible = false">取 消</el-button>
              <el-button type="primary" @click="commitApp('appInfo')">提 交</el-button>
            </span>
          </el-form-item>
        </el-form>
      </div>
    </el-drawer>

    <div class="filter-container">
      <el-form :inline="true" :model="search">
        <el-form-item label="归属项目">
          <el-select v-model="search.productId" clearable>
            <el-option value="" label="所有"></el-option>
            <el-option
              v-for="item in options"
              :key="item.id"
              :label="item.title"
              :value="item.id"
            >
              <span style="float: left">{{ item.keyCode }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px">{{
                item.title
              }}</span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="归属项目ID">
          <el-input
            v-model="search.productId"
            placeholder="请输入归属ID查询"
            style="width: 200px"
            clearable
          />
        </el-form-item>
        <el-form-item label="系统/配置项名称">
          <el-input
            v-model="search.name"
            placeholder="名称模糊查询"
            style="width: 200px"
            clearable
          />
        </el-form-item>
        <br />
        <el-form-item label="描  述">
          <el-input
            v-model="search.note"
            placeholder="描述查询"
            style="width: 210px"
            clearable
          />
        </el-form-item>
        <el-form-item label="测试级别">
          <el-input
            v-model="search.level"
            placeholder="测试级别"
            style="width: 210px"
            clearable
          />
        </el-form-item>
        <el-form-item label="被测类型">
          <el-input
            v-model="search.junstatus"
            placeholder="改造/新研"
            style="width: 210px"
            clearable
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" plain @click="searchClick()">搜索</el-button>
        </el-form-item>
      </el-form>
      <el-button type="primary" icon="el-icon-plus" style="float: right" @click="addApp()"
        >添加配置项/系统</el-button
      >
    </div>
    <!--:data 绑定data()的数组值,会动态根据其变化而变化-->
    <el-table
      :data="tableData"
      border
      :header-cell-style="{ 'text-align': 'center' }"
      :cell-style="{ 'text-align': 'center' }"
    >
      <!--:data prop绑定{}中的key，label为自定义显示的列表头-->
      <el-table-column prop="productId" label="归属项目的ID" />
      <el-table-column prop="name" label="系统/配置项" />
      <el-table-column prop="title" label="归属分类" />
      <el-table-column prop="note" label="被测描述" />
      <el-table-column prop="level" label="被测件级别" />
      <el-table-column prop="junstatus" label="被测件新研/改造" />
      <el-table-column prop="updateUser" label="更新人" />
      <el-table-column :formatter="formatDate" prop="updateDate" label="更新时间" />
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-link icon="el-icon-edit" @click="updateApp(scope.row)">修改</el-link>
        </template>
      </el-table-column>
    </el-table>
    <br />
    <div>
      <el-pagination
        background
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="search.currentPage"
        :page-size="search.pageSize"
        layout="total, sizes, prev, pager, next"
        :page-sizes="[5, 10, 20, 30, 50]"
        :total="total"
      >
      </el-pagination>
    </div>
  </div>
</template>

<script>
import moment from "moment";
import { apiAppsProduct, apiAppsSearch, apiAppsCommit } from "@/api/apps";
import store from "@/store";

export default {
  name: "Apps",
  data() {
    return {
      //获得登录人名字
      op_user: store.getters.name,
      //定义修改或新增动作
      appAction: "ADD",
      //控制抽屉显示与否
      drawerVisible: false,
      //添加或修改配置项系统object
      appInfo: {
        id: "",
        name: "",
        productId: "",
        note: "",
        level: "",
        junstatus: "",
        producer: "",
        creteUser: "",
        updateUser: "",
      },
      //规则定义非空
      rules: {
        name: [{ required: true, message: "请输入配置项或系统名称", trigger: "blur" }],
        productId: [{ required: true, message: "请确认所属项目", trigger: "blur" }],
        level: [{ required: true, message: "请选择配置项还是系统", trigger: "blur" }],
        junstatus: [{ required: true, message: "请选择是新研还是改造", trigger: "blur" }],
        producer: [{ required: true, message: "请填写负责人名称", trigger: "blur" }],
      },

      search: {
        productId: "",
        name: "",
        note: "",
        level: "",
        junstatus: "",
        pageSize: 10,
        currentPage: 1,
      },
      options: [],
      total: 1,
      tableData: [],
    };
  },
  // 页面生命周期中的创建阶段调用
  created() {
    // 调用methods的方法，即初次加载就请求数据
    this.productList();
    this.searchClick();
  },
  methods: {
    formatDate(row, column) {
      const date = row[column.property];
      if (date === undefined) {
        return "";
      }
      // 使用moment格式化时间，由于我的数据库是默认时区，偏移量设置0，各自根据情况进行配置
      return moment(date).utcOffset(0).format("YYYY-MM-DD HH:mm");
    },
    productList() {
      apiAppsProduct().then((resp) => {
        this.options = resp.data;
      });
    },
    searchClick() {
      apiAppsSearch(this.search).then((response) => {
        // 将返回的结果赋值给表格自动匹配
        this.tableData = response.data;
        this.total = response.total;
      });
    },
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`);
      this.search.pageSize = val;
      this.searchClick();
    },
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`);
      this.search.currentPage = val;
      this.searchClick();
    },
    addApp() {
      // 定义动作，以抽屉做判断
      this.appAction = "ADD";
      //添加数据初始化
      this.appInfo.name = "";
      this.appInfo.productId = "";
      this.appInfo.note = "";
      this.appInfo.level = "";
      this.appInfo.junstatus = "";
      this.appInfo.producer = "";
      this.appInfo.creteUser = this.op_user;
      this.appInfo.updateUser = this.op_user;
      //初始化完成后显示抽屉
      this.drawerVisible = true;
      //如果有遗留则验证清空
      // this.$nextTick(() => {
      //   this.$refs["appInfo"].resetFields();
      // });
    },
    updateApp(row) {
      this.appAction = "UPDATE";
      this.drawerVisible = true;
      this.appInfo.id = row.id;
      this.appInfo.name = row.name;
      this.appInfo.productId = row.productId;
      this.appInfo.note = row.note;
      this.appInfo.level = row.level;
      this.appInfo.junstatus = row.junstatus;
      this.appInfo.producer = row.producer;
      this.appInfo.creteUser = "";
      this.appInfo.updateUser = this.op_user;
    },
    commitApp() {
      //上面form定义ref，前端验证通过代码如下
      this.$refs["appInfo"].validate((valid) => {
        if (valid) {
          this.appInfo.updateUser = this.op_user;
          apiAppsCommit(this.appInfo).then((response) => {
            // 如果request.js没有拦截即表示成功，给出对应提示和操作
            this.$notify({
              title: "成功",
              message: this.appAction === "ADD" ? "应用添加成功" : "应用修改成功",
              type: "success",
            });
            // 关闭对话框
            this.drawerVisible = false;
            // 重新查询刷新数据显示
            this.productList();
          });
        } else {
          return false;
        }
      });
      //关闭抽屉
      this.drawerVisible = false;
      //重新查询应用
      this.productList();
    },
  },
};
</script>

<style scoped>
.el-pagination {
  text-align: right;
}
</style>
