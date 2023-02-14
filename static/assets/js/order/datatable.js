$(document).ready(function () {
    const fresh = () => {
        // debugger
        let sumSubTotal = 0
        let obj = $("#myTable").find("tbody").children("tr")
        let localTableData = {}
        $(obj).each(function (i, v) {
            // debugger

            let bookId = $("td", v).eq(0).attr("data-bookId")
            let price = $("td", v).eq(3).attr("data-value")
            let amount = $("td", v).eq(4).attr("data-value")
            $("td", v).eq(5).html(`<span class="bt-content">${price * amount}</span>`)
            $("td", v).eq(5).attr("data-value",price * amount)
            sumSubTotal += price * amount

            localTableData[bookId] = amount
        });
        // debugger
        localStorage.setItem("localTableData", JSON.stringify(localTableData))
        $("#total").html(`<span class="bt-content">${sumSubTotal}</span>`);
    }
    let dataset = []
    $.ajax({
        type: "GET",
        url: "/api/get_book_info",
        data: {},
        async: false,
        dataType: "json",
        success: function (response) {
        //   書籍id name subject details price img
        console.log(response)
        dataset = response
        }
    });
    function getCookie(name) {
    const parts = `; ${document.cookie}`.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    }
    
    var  bookAmount = {}
    $.ajax({
        type: "GET",
        url: "/api/get_order_by_stuId",
        data: {},
        async: false,
        dataType: "json",
        success: function (response) {
            response.bookName.forEach((x,i) => {
                bookAmount[x[0]] = response.data.filter(x => x[2] == getCookie("stuId"))[0][i+3]
            });
            console.log(bookAmount)
        }
    });
    
    $('#myTable').DataTable({
        "paging": false, // 預設為true 分頁功能，若要開啟不用特別設定
        "lengthMenu": ["All"], //顯示筆數設定 預設為[10, 25, 50, 100]
        "pageLength": 'All',// 預設為'10'，若需更改初始每頁顯示筆數，才需設定
        "info": false,
        "columnDefs": [{
            "targets": [2, 4],
            "orderable": false,
        }, {
            "width": "20%", "targets": [0, 1, 2, 3, 4, 5]
        }
        ],
        "oLanguage": {
            "sSearch": "搜尋書籍: "
        },
        "language": {
            searchPlaceholder: "小黃書"
        },
        // "ajax": {
        //     "url": "/api/get_book_info",
        //     "type": "GET",
        //     "data": function ( d ) {
        //         console.log(d)
        //         return ""
        //         // return $.extend( {}, d, {
        //         //     "extra_search": $('#extra').val()
        //         // } );
        //     }
        // },
        "data": dataset.map((x) => [
            x[1], //name
            x[2], //科目
            x[3], //details
            x[4], //price
            1, //數量
            x[4], //數量

        ]),
        "createdRow": function (row, data, dataIndex) {
            let nowbookId = `${dataset[dataIndex][0]}`
            $('td', row).eq(0).each(function () {
                $(this).attr("data-bookId", `${nowbookId}`)
            })
            $('td', row).eq(3).each(function () {
                $(this).attr("data-value", $(this).html())
            })
            $('td', row).eq(5).each(function () {
                $(this).attr("data-value", $(this).html())
            })
            $('td', row).eq(4).each(function () {
                $(this).attr("data-value", $(this).html())
                if (getCookie("stuId") == undefined){

                    if (localStorage.getItem("localTableData") == null){
                        $(this).attr("data-value", $(this).html())
                    }else {
                        $(this).attr("data-value", JSON.parse(localStorage.getItem("localTableData"))[nowbookId])
                        $(this).html(JSON.parse(localStorage.getItem("localTableData"))[nowbookId])
                    }
                }else{
                    $(this).attr("data-value", bookAmount[nowbookId])
                    $(this).html(bookAmount[nowbookId])
                }


                $(this).attr("data-mode", "view")
                $(this).css("padding", "0");
            })
            $('td', row).eq(4).click(function (e) {
                e.preventDefault();
                if ($(this).attr("data-mode") == "input") {
                    return
                }
                $(this).attr("data-mode", "input")
                $(this).html(`<input type="number" min="0" max="5" value="${$(this).attr("data-value")}" class="w-full">`);
                // $(this).html(`<input type="number" value="${amount}">`);
            }).focusout(function () {

                if ($(this).attr("data-mode") == "view") {
                    return
                }
                $(this).attr("data-mode", "view")
                $(this).attr("data-value", $(this).children("input").val() > 5 || $(this).children("input").val() < 0 ? $(this).attr("data-value") : $(this).children("input").val() == "" ? 0 : $(this).children("input").val())
                $(this).html(`<span class="bt-content">${$(this).attr("data-value")}</span>`);

                fresh()
            });
        }
    });
    fresh()

});