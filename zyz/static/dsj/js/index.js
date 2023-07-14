window.onload = function () {
  // 时间
  Time();
  // 图表
  tu_biao();
}

// 时间
function Time() {
  (function () {
    function updateTime() {
      const now = new Date();

      const year = now.getFullYear();
      const month = now.getMonth() + 1; // 月份从0开始计数，所以要加1
      const day = now.getDate();
      const hour = now.getHours();
      const minute = now.getMinutes();
      const second = now.getSeconds();

      const timeElement = document.querySelector(".showTime");
      timeElement.textContent = `${year}年${month}月${day}日 ${hour}时:${minute}分:${second}秒`;
    }

    setInterval(updateTime, 1000); // 每隔1秒更新一次时间
  })();
}

// 图表
function tu_biao() {


  (function () {
    // 初始化 echarts 实例对象
    const myChart = echarts.init(document.querySelector(".map .chart"));

    // 用 XMLHttpRequest 加载湖南省地图数据
    const xhr = new XMLHttpRequest();
    xhr.open('GET', 'https://geo.datav.aliyun.com/areas_v3/bound/430000_full.json', true);
    xhr.onload = function () {
      if (xhr.status === 200) {
        let geoJson = JSON.parse(xhr.responseText);
        // 注册地图
        echarts.registerMap('湖南', geoJson);
        // 绘制地图
        myChart.setOption({
          title: {
            text: '湖南省地图',
            textStyle: {
              color: '#4c9bfd'
            }
          },
          tooltip: {
            trigger: 'item',
          },
          series: [
            {
              name: '',
              type: 'map',
              map: '湖南',
              zoom: 1.2,//缩放级别
              roam: true, //开启地图的平移和缩放
              data: [
                { name: '长沙市', value: 100 },
                { name: '株洲市', value: 200 },
                { name: '湘潭市', value: 300 },
                { name: '衡阳市', value: 400 },
                { name: '邵阳市', value: 500 },
                { name: '岳阳市', value: 600 },
                { name: '常德市', value: 700 },
                { name: '张家界市', value: 800 },
                { name: '益阳市', value: 900 },
                { name: '郴州市', value: 1000 },
                { name: '永州市', value: 1100 },
                { name: '怀化市', value: 1200 },
                { name: '娄底市', value: 1300 },
                { name: '湘西土家族苗族自治州', value: 1400 }
              ],
              itemStyle: {
                normal: {
                  label: {
                    show: true, //显示省份标签
                    textStyle: { color: "#fff" } //省份标签字体颜色
                  },
                  borderWidth: 1, //区域边框宽度
                  borderColor: '#fff', //区域边框颜色
                  areaColor: 'rgba(0, 170, 255, 0.3)'  //区域填充颜色，这里的颜色为透明淡蓝色
                },
                emphasis: {
                  label: {
                    show: true,
                    textStyle: {
                      color: "#FFF",
                      fontSize: '20'
                    }
                  },
                  borderWidth: 2,
                  borderColor: '#fff',
                  areaColor: 'rgba(0, 170, 255, 0.6)'
                }
              },
            }
          ],
          //添加地图缩放控件
          visualMap: {
            type: 'continuous',
            min: 0,
            max: 1400,
            left: 'left',
            bottom: 'bottom',
            inRange: {
              color: ['#e0ffff', '#006edd']
            },
            text: ['高', '低'],
            calculable: true, 
            textStyle: {
              color: '#4c9bfd'
            }
          }
        });
      } else {
        console.log('地图数据暂无！');
      }
    };
    xhr.send();
    window.addEventListener('resize', function () {
      myChart.resize();
    })
  })();

  //带背景色的柱状图
  (function () {
    var myChart = echarts.init(document.querySelector('.bar .chart'));

    var option = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      grid: {
        left: '10%',
        top: '10px',
        right: '10%',
        bottom: '4%',
        containLabel: true
      },
      xAxis: [
        {
          type: 'category',
          data: ['进社区农村', '进家庭', '进托育机构'],
          axisTick: {
            alignWithLabel: true
          },
          axisLabel: {
            color: "rgba(255,255,255,.6)",
            fontSize: "11"
          },
          axisLine: {
            show: false
          }
        }
      ],
      yAxis: [
        {
          type: 'value',
          axisLabel: {
            color: "rgba(255,255,255,.6)",
            fontSize: "12"
          },
          axisLine: {
            lineStyle: {
              color: "rgba(255,255,255,.1)",
              width: "2"
            }
          },
          splitLine: {
            lineStyle: {
              color: "rgba(255,255,255,.1)"
            }
          }
        }
      ],
      series: [
        {
          name: '直接访问',
          type: 'bar',
          barWidth: '35%',
          data: [100, 53, 200],
          itemStyle: {
            barBorderRadius: 5
          }
        }
      ],
      color: ["#2f89cf"]
    };
    myChart.setOption(option);

    window.addEventListener('resize', function () {
      myChart.resize();
    });
  })();

  (function () {
    var myChart = echarts.init(document.querySelector('.bar2 .chart'));

    var option = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      grid: {
        left: '0%',
        top: '10px',
        right: '0%',
        bottom: '4%',
        containLabel: true
      },
      yAxis: [
        {
          type: 'category',
          data: ['移动幼儿课堂', '照护技能小剧场', '儿童非遗文化传承展示'],
          axisLabel: {
            color: "rgba(255,255,255,.6)",
            fontSize: "12"
          },
          axisLine: {
            show: false
          },
          axisTick: {
            show: false
          }
        }
      ],
      xAxis: [
        {
          type: 'value',
          axisLabel: {
            color: "rgba(255,255,255,.6)",
            fontSize: "12"
          },
          axisLine: {
            lineStyle: {
              color: "rgba(255,255,255,.1)",
              width: "2"
            }
          },
          splitLine: {
            lineStyle: {
              color: "rgba(255,255,255,.1)"
            }
          }
        }
      ],
      series: [
        {
          name: '直接访问',
          type: 'bar',
          barWidth: '35%',
          data: [100, 53, 200],
          itemStyle: {
            barBorderRadius: 5
          }
        }
      ],
      color: ["#2f89cf"]
    };
    myChart.setOption(option);

    window.addEventListener('resize', function () {
      myChart.resize();
    });
  })();


  // 折线图模块1
  (function () {
    // 年份对应数据
    var yearData = [{
      data: [
        // 两个数组是因为有两条线
        [24, 40, 101, 134, 90, 230, 210, 230, 120, 230, 210, 120],
        [40, 64, 191, 324, 290, 330, 310, 213, 180, 200, 180, 79],
        [50, 60, 101, 324, 190, 310, 190, 213, 170, 210, 170, 70]
      ]
    }
    ];

    var myChart = echarts.init(document.querySelector(".line .chart"));

    var option = {
      // 修改两条线的颜色
      color: ['#00f2f1', '#ed3f35', '#ed6f35'],
      tooltip: {
        trigger: 'axis'
      },
      // 图例组件
      legend: {
        // 当serise 有name值时， legend 不需要写data
        // 修改图例组件文字颜色
        textStyle: {
          color: '#4c9bfd'
        },
        right: '5%',
      },
      grid: {
        top: "20%",
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true,
        show: true, // 显示边框
        borderColor: '#012f4a' // 边框颜色
      },
      xAxis: {
        type: 'category',
        boundaryGap: false, // 去除轴间距
        data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
        // 去除刻度线
        axisTick: {
          show: false
        },
        axisLabel: {
          color: "#4c9bfb" // x轴文本颜色
        },
        axisLine: {
          show: false // 去除轴线
        }
      },
      yAxis: {
        type: 'value',
        // 去除刻度线
        axisTick: {
          show: false
        },
        axisLabel: {
          color: "#4c9bfb" // x轴文本颜色
        },
        axisLine: {
          show: false // 去除轴线
        },
        splitLine: {
          lineStyle: {
            color: "#012f4a"
          }
        }
      },
      series: [{
        type: 'line',
        smooth: true, // 圆滑的线
        name: '社区乡村小分队',
        data: yearData[0].data[0]
      },
      {
        type: 'line',
        smooth: true, // 圆滑的线
        name: '托育机构小分队',
        data: yearData[0].data[1]
      },
      {
        type: 'line',
        smooth: true, // 圆滑的线
        name: '入户小分队',
        data: yearData[0].data[2]
      }
      ]
    };

    myChart.setOption(option);

    // 4.让图表随屏幕自适应
    window.addEventListener('resize', function () {
      myChart.resize();
    })
  })();

  // 雷达图图模块
  (function () {
    var myChart = echarts.init(document.querySelector('.line2 .chart'));

    var option = {
      legend: {
        data: ['专业分布'],
        textStyle: {
          color: '#4c9bfd'
        }, right: '5%',
      },
      radar: {
        shape: 'circle',
        indicator: [
          { name: '数字媒体技术', max: 100 },
          { name: '云计算技术应用', max: 100 },
          { name: '软件技术', max: 100 },
          { name: '电子商务', max: 100 },
          { name: '现代教育技术', max: 100 },
          { name: '美术教育', max: 100 },
          { name: '舞蹈教育', max: 100 },
          { name: '视觉传达设计', max: 100 },
          { name: '舞蹈表演', max: 100 },
          { name: '动漫设计', max: 100 },
          { name: '早期教育', max: 100 },
          { name: '学前教育', max: 100 },
          { name: '婴幼儿托育服务与管理', max: 100 },
          { name: '体育教育', max: 100 }
        ],
        axisLine: {
          show: false
        },
        splitLine: {
          lineStyle: {
            color: 'rgba(255, 255, 255, 0.2)',
            width: 1
          }
        },
        splitArea: {
          show: true,
          areaStyle: {
            color: [
              'rgba(0, 128, 255, 0.3)',
              'rgba(0, 128, 255, 0.2)',
              'rgba(0, 128, 255, 0.1)'
            ]
          }
        },
        name: {
          textStyle: {
            color: '#fff'
          }
        },
        radius: '60%'
      },
      series: [
        {
          name: 'Budget vs spending',
          type: 'radar',
          lineStyle: {
            width: 3,
            color: 'rgba(0, 128, 255, 0.5)'
          },
          itemStyle: {
            color: '#00b0ff'
          },
          emphasis: {
            lineStyle: {
              width: 4,
              color: '#00b0ff'
            }
          },
          data: [
            {
              value: [80, 50, 80, 50, 40, 45, 50, 70, 50, 45, 48, 45, 73, 45],
              name: '专业分布'
            }
          ]
        }
      ]
    };

    myChart.setOption(option);

    window.addEventListener('resize', function () {
      myChart.resize();
    });
  })();

  // 饼形图1
  (function () {
    var myChart = echarts.init(document.querySelector(".pie .chart"));
    var option = {
      color: ["#1089E7", "#F57474", "#56D0E3", "#F8B448", "#8B78F6"],
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
      },
      legend: {
        // 垂直居中,默认水平居中
        // orient: 'vertical',

        bottom: 0,
        left: 10,
        // 小图标的宽度和高度
        itemWidth: 10,
        itemHeight: 10,
        // 修改图例组件的文字为 12px
        textStyle: {
          color: "rgba(255,255,255,.5)",
          fontSize: "15"
        }
      },
      series: [{
        name: '4个体系',
        type: 'pie',
        // 设置饼形图在容器中的位置
        center: ["50%", "42%"],
        // 修改饼形图大小，第一个为内圆半径，第二个为外圆半径
        radius: ['40%', '60%'],
        avoidLabelOverlap: false,
        // 图形上的文字
        label: {
          show: false,
          position: 'center'
        },
        // 链接文字和图形的线
        labelLine: {
          show: false
        },
        data: [{
          value: 1,
          name: "孵化体系"
        },
        {
          value: 4,
          name: "教学体系"
        },
        {
          value: 2,
          name: "课程体系"
        },
        {
          value: 2,
          name: "管理体系"
        }
        ]
      }]
    };

    myChart.setOption(option);
    window.addEventListener('resize', function () {
      myChart.resize();
    })
  })();

  // 饼形图2
  (function () {
    var myChart = echarts.init(document.querySelector('.pie2 .chart'));
    var option = {
      color: ['#60cda0', '#ed8884', '#ff9f7f', '#0096ff', '#9fe6b8', '#32c5e9', '#1d9dff'],
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b} : {c} ({d}%)'
      },
      legend: {
        bottom: 0,
        itemWidth: 10,
        itemHeight: 10,
        textStyle: {
          color: "rgba(255,255,255,.5)",
          fontSize: 10
        }
      },
      series: [{
        name: '地区分布',
        type: 'pie',
        radius: ["10%", "60%"],
        center: ['50%', '40%'],
        // 半径模式  area面积模式
        roseType: 'radius',
        // 图形的文字标签
        label: {
          fontsize: 10
        },
        // 引导线调整
        labelLine: {
          // 连接扇形图线长(斜线)
          length: 6,
          // 连接文字线长(横线)
          length2: 8
        },
        data: [{
          value: 50,
          name: '长沙市'
        },
        {
          value: 24,
          name: '株洲市'
        },
        {
          value: 25,
          name: '湘潭市'
        },
        {
          value: 20,
          name: '衡阳市'
        },
        {
          value: 25,
          name: '邵阳市'
        },
        {
          value: 30,
          name: '岳阳市'
        },
        {
          value: 42,
          name: '常德市'
        },
        {
          value: 32,
          name: '张家界市'
        },
        {
          value: 45,
          name: '益阳市'
        },
        {
          value: 51,
          name: '郴州市'
        },
        {
          value: 57,
          name: '永州市'
        },
        {
          value: 40,
          name: '怀化市'
        },
        {
          value: 34,
          name: '娄底市'
        },
        {
          value: 19,
          name: '湘西土家族苗族自治州'
        }
        ]
      }]
    };

    myChart.setOption(option);
    window.addEventListener('resize', function () {
      myChart.resize();
    })
  })();

}