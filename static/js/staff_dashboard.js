function get_data() {
    $.ajax({
        url: '/get-chart-data/',
        error: function () {
            console.log("error");
        },
        success: function (sdata) {
            var status = sdata.labels;
            var count = sdata.data;
            bgcolors = [];
            hbcolors = [];
            bdrcolors = [];
            var dynamicColors = function () {
                var r = Math.floor(Math.random() * 255);
                var g = Math.floor(Math.random() * 255);
                var b = Math.floor(Math.random() * 255);
                bgcolors.push("rgba(" + r + "," + g + "," + b + ",0.75)");
                hbcolors.push("rgba(" + r + "," + g + "," + b + ",1)");
                bdrcolors.push("rgba(255,255,255)");
            };

            for (var i in status) {
                dynamicColors();
            }

            var chardata = {
                labels: status,
                datasets: [
                    {
                        backgroundColor: bgcolors,
                        borderColor: bdrcolors,
                        hoverBackgroundColor: hbcolors,
                        hoverBorderColor: bdrcolors,
                        data: count
                    }
                ]
            };
            var options = {
                title: {
                    text: 'Top 10 Ordered Books',
                    display: false,
                    position: 'top',
                },
                responsive: false,
                legend: {
                    display: true,
                    position: 'right',
                },


            };
            var ctx = $("#issued-books");
            var barGraph = new Chart(ctx, {
                type: 'pie',
                data: chardata,
                options: options
            });

        },
        type: 'GET'
    });
}

async function asyncCall() {
    var result = await get_data();
}

asyncCall();