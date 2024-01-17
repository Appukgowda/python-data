<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://d3js.org/d3.v7.min.js"></script>
</head>
<body>
    <!-- Button to update data -->
    <button id="updateData">Update Data</button>
    <!-- Input for selecting town count -->
    <input type="range" id="town-count" min="1" max="500" value="50">
    <!-- SVG element for the map -->
    <svg id="map">
        <image xlink:href="united-kingdom.svg" width="100%" height="100%"></image>
    </svg>

    <script>
        //References:
        //https://observablehq.com/@d3/gallery?utm_source=d3js-org&utm_medium=nav&utm_campaign=try-observable
        // Define SVG dimensions
        const mapWidth = 900;
        const mapHeight = 1100;

        // Select the SVG element
        const mapSvg = d3.select("#map")
            .attr("width", mapWidth)
            .attr("height", mapHeight);

        // Define the map projection
        const mapProjection = d3.geoAlbers()
            .center([0, 55.4])
            .rotate([3.4, 0])
            .scale(6000)
            .translate([mapWidth / 2, mapHeight / 2]);

        // Create a path generator based on the projection
        const mapPath = d3.geoPath().projection(mapProjection);

        // Creating a group for circles and labels
        const mapGroup = mapSvg.append("g");

        // Function to plot towns on the map
        function plotMapTowns(cityData) {
            // Remove existing circles and labels
            mapSvg.selectAll("circle")
                .transition()
                .duration(500)
                .attr("r", 0)
                .remove()
                .end()
                .then(function() {
                    // Add new circles towns
                    const townCircles = mapGroup.selectAll("circle")
                        .data(cityData)
                        .enter()
                        .append("circle")
                        .attr("cx", d => mapProjection([d.lng, d.lat])[0])
                        .attr("cy", d => mapProjection([d.lng, d.lat])[1])
                        .attr("r", 0)
                        .style("fill", "blue")
                        .style("stroke", "white");

                    // Transition to display circles
                    townCircles.transition()
                        .duration(500)
                        .attr("r", 5);

                    // Add text labels for towns
		    //Used chatgpt to add functionality to label the towns
                    const townLabels = mapGroup.selectAll("text")
                        .data(cityData)
                        .enter()
                        .append("text")
                        .attr("x", d => mapProjection([d.lng, d.lat])[0])
                        .attr("y", d => mapProjection([d.lng, d.lat])[1])
                        .attr("dy", -10)
                        .text(d => `${d.Town}, Population: ${d.Population}`)
                        .style("fill", "black")
                        .style("font-size", "12px");

                    // Add tooltips to circles
                    townCircles.append("title").text(d => `${d.Town}, Population: ${d.Population}`);
                });
        }

        // Function to handle data update based on the slider input
        function handleDataUpdate() {
            const numTowns = document.getElementById("town-count").value;
            d3.json(`http://34.38.72.236/Circles/Towns/${numTowns}`).then(plotMapTowns);
        }

        // Event listener for slider input
        d3.select("#town-count").on("input", handleDataUpdate);

        // Initial data load and plot
        d3.json("http://34.38.72.236/Circles/Towns/50").then(plotMapTowns);

        // Event listener for updating data when the button is clicked
        d3.select("#updateData").on("click", function () {
            d3.json("http://34.38.72.236/Circles/Towns/50").then(plotMapTowns);
        });
    </script>
</body>
</html>
