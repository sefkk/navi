
window.onload = function() { 
        
    const generateMapButton = document.getElementById("generate-map-btn");
    const findPathButton = document.getElementById("find-path-btn");
    const travelModeDiv = document.querySelector(".radio-inputs");
    const algorithmChoiceDiv = document.querySelector(".algorithm-choice");
    const priorityDiv = document.querySelector(".priority");
    const resultsDiv = document.getElementById("results"); 
    const canvas = document.querySelector(".map");
    const ctx = canvas.getContext("2d");
    const onCanvasText = document.querySelector(".on-canvas");

    const resetPathButton = document.getElementById("reset-path-btn");

    // Declare variables first
    let mapData = null;
    let startNode = null; 
    let endNode = null;
    
    // Default Values 
    let algorithm = "dijkstra"; 
    let travelMode = "car"; 
    let selectedPriority = 'distance';
    
    let imgHouse = new Image();
    imgHouse.src = '/static/img/house-big.png'; 
    let imgSize = 64; 

    let imgLandcape = new Image();
    imgLandcape.src = '/static/img/landscape-4.png'; 
    // imgLandcape.src = 'static/img/a.png'; 
    // let imgSizeLand = 64; 

    travelModeDiv.addEventListener("click", function(event) {
        if (event.target.type === "radio") {
            travelMode = event.target.value;
            console.log("Travel mode is:", travelMode);
        }
    });

    algorithmChoiceDiv.addEventListener("click", function(event) {
        if (event.target.type === "radio") {
            algorithm = event.target.value; 
            console.log("selected algorithm is:", algorithm);
        }
    }); 

    priorityDiv.addEventListener("click", function(event) {
        if (event.target.type === "radio") {
            selectedPriority = event.target.value;
            console.log("selected priority is:", selectedPriority);
        }
    }); 

    generateMapButton.addEventListener("click", async function getMapData() {
        try {
            // Get current canvas dimensions for responsive map generation
            const canvasWidth = canvas.offsetWidth;
            const canvasHeight = canvas.offsetHeight;
            const response = await fetch(`/generate_map?width=${canvasWidth}&height=${canvasHeight}`);
            mapData = await response.json();
            console.log("DATA", mapData); // The map data from the server
            drawMap(mapData); // Pass the data to the drawMap function
        } catch (error) {
            console.error('Error fetching data:', error); 
        }

        onCanvasText.classList.remove("visible");
        onCanvasText.classList.add("hidden");
        
        // 1. Reset the global variables
        startNode = null;
        endNode = null;
        console.log("Path has been reset. Start a new selection.");
        
        // 2. Clear any old results displayed on the page
        resultsDiv.style.transition = 'opacity 0.3s ease';
        resultsDiv.style.opacity = '0';
        setTimeout(() => {
            resultsDiv.innerHTML = `
                <h3>Path Details</h3>
                <p><strong>Distance:</strong> <span id="distance">--</span></p>
                <p><strong>Time:</strong> <span id="time">--</span></p>
                <p><strong>Cost:</strong> <span id="cost">--</span></p>
            `;
            resultsDiv.style.opacity = '1';
        }, 300);

        // 3. Redraw the map to remove the old path and highlights
        if (mapData) {
            drawMap(mapData);
        } else {
            // If the map data is gone, just clear the canvas completely
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        }
    }); 

    function drawLandscape(ctx, width, height) {
        // // You can define a color palette for your terrain
        // const colors = {
        //     land: '#a7a99dff', // A muted green/gray for the land
        //     // grass: '#799e6aff', // A fresh green for grassy areas
        //     // water: '#4f81c7ff', // A fresh blue for the water 
        //     // sand: '#d2b48cff', // A sandy color for beaches 
        //     // building: '#bb5858ff', // A dark gray for building rooftops
        //     // buildingCluster: '#dcdcdcff' // A slightly lighter gray for variety
        // };

        // // Draw the entire background as a base color 
        // ctx.fillStyle = colors.land; 
        // ctx.fillRect(0, 0, width, height);

        // // Draw a few random "terrain" rectangles on top
        // for (let i = 0; i < 120; i++) {
        //     const keys = Object.keys(colors);
        //     const randomKey = keys[Math.floor(Math.random() * keys.length)];
        //     ctx.fillStyle = colors[randomKey];
            
        //     const x = Math.random() * width;
        //     const y = Math.random() * height;
        //     const w = Math.random() * 30 + Math.random() * 35;
        //     const h = Math.random() * 30 + Math.random() * 35;
            
        //     ctx.fillRect(x, y, w, h);
        // }

        ctx.drawImage(imgLandcape, 0, 0, width, height); 
    };


    function getRoadColor(traffic) {
        // Traffic is a value between 1.0 and 2.75
        // We can map this to a darkness scale
        if (traffic >= 2.4) {
            return '#8B0000'; // very dark red for extreme traffic
        } else if (traffic >= 2.05) { 
            return '#D64124'; // dark red for very high traffic
        } else if (traffic >= 1.7) {
            return '#DBAE25'; // orange for high traffic
        } else if (traffic >= 1.35) {
            return '#4a922eff'; // yellow-green for moderate traffic
        } else {
            return '#5dcc2aff'; // green for low traffic
        }
    }

    function drawMap(data) {
        console.log("Drawing map with data:", data);

        // Clear the canvas and draw the landscape first
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawLandscape(ctx, canvas.width, canvas.height);

        // Enable anti-aliasing and smooth rendering
        ctx.imageSmoothingEnabled = true;
        ctx.imageSmoothingQuality = 'high';
        
        // Set line properties for smooth edges
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        ctx.miterLimit = 10;

        // Draw all edges (roads) with improved rendering
        data.edges.forEach(edge => {
            const fromNode = data.nodes.find(n => n.id === edge.from);
            const toNode = data.nodes.find(n => n.id === edge.to);
            
            if (!fromNode || !toNode) return;
            
            const baseWidth = edge.highway ? 20 : 13;
            const topWidth = edge.highway ? 13 : 9;
            const shadowWidth = baseWidth + 2;
            
            // Draw shadow/outline for depth
            ctx.beginPath();
            ctx.moveTo(fromNode.x, fromNode.y);
            ctx.lineTo(toNode.x, toNode.y);
            ctx.lineWidth = shadowWidth;
            ctx.strokeStyle = 'rgba(0, 0, 0, 0.3)';
            ctx.shadowBlur = 3;
            ctx.shadowColor = 'rgba(0, 0, 0, 0.2)';
            ctx.stroke();
            ctx.shadowBlur = 0;
            
            // Draw base dark layer with smooth edges
            ctx.beginPath();
            ctx.moveTo(fromNode.x, fromNode.y);
            ctx.lineTo(toNode.x, toNode.y);
            ctx.lineWidth = baseWidth;
            ctx.strokeStyle = '#1a1a1a';
            ctx.stroke(); 

            // Draw top colored layer with smooth edges
            ctx.beginPath();
            ctx.moveTo(fromNode.x, fromNode.y);
            ctx.lineTo(toNode.x, toNode.y);
            ctx.lineWidth = topWidth;
            ctx.strokeStyle = getRoadColor(edge.traffic);
            ctx.stroke();
        });
        
        // Draw nodes on top of the roads
        data.nodes.forEach(node => {
        // ctx.beginPath();

        // // Customizing the visual style 
        // if (node.is_highway) {
        //     // Style for highway nodes
        //     ctx.arc(node.x, node.y, 6, 0, 2 * Math.PI); // Larger radius
        //     ctx.fillStyle = '#2b2727ff'; // Dark color
        //     ctx.lineWidth = 0.3;
        //     ctx.strokeStyle = '#fff'; // White border
        // } else {
        //     // Style for regular nodes
        //     ctx.arc(node.x, node.y, 3, 0, 2 * Math.PI); // Smaller radius
        //     ctx.fillStyle = '#757171ff'; // Light gray color
        //     ctx.lineWidth = 0.3;
        //     ctx.strokeStyle = '#fff'; // White border
        // }
        ctx.drawImage(imgHouse, node.x - imgSize/2, node.y - imgSize/2, imgSize, imgSize);

        // Applying the styles to the current node
        // ctx.fill();
        // ctx.stroke();
    });
    }

    // Handle both click and touch events for mobile support
    function handleCanvasInteraction(event) {
        if (!mapData) {
            alert("Please generate a map first.");
            return;
        }

        // Prevent default touch behavior (scrolling, zooming)
        if (event.type === 'touchstart' || event.type === 'touchend') {
            event.preventDefault();
        }

        const rect = canvas.getBoundingClientRect();
        // Get coordinates from either mouse or touch event
        const clientX = event.clientX || (event.touches && event.touches[0]?.clientX) || (event.changedTouches && event.changedTouches[0]?.clientX);
        const clientY = event.clientY || (event.touches && event.touches[0]?.clientY) || (event.changedTouches && event.changedTouches[0]?.clientY);
        
        if (!clientX || !clientY) return;
        
        const x = clientX - rect.left;
        const y = clientY - rect.top;

        const clickedNode = mapData.nodes.find(node => {
            const distance = Math.sqrt(Math.pow(node.x - x, 2) + Math.pow(node.y - y, 2));
            // Increase touch target size on mobile
            const touchThreshold = window.innerWidth <= 768 ? 20 : 10;
            return distance < touchThreshold;
        });

        if (clickedNode) {
            if (!startNode) {
                // First click: select the start node
                startNode = clickedNode;
                drawMap(mapData); // Redraw to clear previous selections
                drawSelection(startNode, 'green');
                console.log("Start Node selected:", startNode.id);
            } else if (!endNode && clickedNode.id !== startNode.id) {
                // Second click: select the end node (if it's not the same as start)
                endNode = clickedNode;
                drawSelection(endNode, 'red');
                console.log("End Node selected:", endNode.id);
                // Now the user can click the "Calculate Path" button
            }
        }
    }
    
    // Add event listeners for both mouse and touch
    canvas.addEventListener('click', handleCanvasInteraction);
    canvas.addEventListener('touchend', handleCanvasInteraction);

    // A small helper function to draw the selection circle
    function drawSelection(node, color) {
        ctx.beginPath();
        ctx.arc(node.x, node.y, 25, 0, 2 * Math.PI);
        ctx.strokeStyle = color;
        ctx.lineWidth = 4;
        ctx.shadowBlur = 10;
        ctx.shadowColor = color;
        ctx.stroke();
        ctx.shadowBlur = 0; // Reset shadow
    }
    
    // Function to resize canvas (defined after all dependencies)
    function resizeCanvas() {
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width;
        canvas.height = rect.height;
        
        // Redraw map if it exists
        if (mapData) {
            drawMap(mapData);
            // Redraw path if it exists
            if (startNode && endNode) {
                drawSelection(startNode, 'green');
                drawSelection(endNode, 'red');
            }
        }
    }
    
    // Set initial canvas size
    resizeCanvas();
    
    // Handle window resize and orientation change
    window.addEventListener('resize', resizeCanvas);
    window.addEventListener('orientationchange', () => {
        setTimeout(resizeCanvas, 100); // Small delay for orientation change
    });



    findPathButton.addEventListener('click', async () => {
        // Check if the necessary data is available
        if (!mapData) {
            alert('Please generate a map first.');
            return;
        }
        if (!startNode || !endNode) {
            alert('Please select both a start and an end point on the map.');
            return;
        }

        try {
            // Send a POST request to the backend to find the path
            const response = await fetch('/find_path', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    start_node_id: startNode.id,
                    end_node_id: endNode.id,
                    algorithm: algorithm,
                    priority: selectedPriority,
                    travel_mode: travelMode,
                })
            });

            // Parse the JSON response from the server
            const result = await response.json();
            
            if (result.error) {
                alert(result.error);
                console.error(result.error);
                return;
            }

            // Draw the path and display the results
            drawPath(result.path);
            displayResults(result);
            console.log('Path calculation successful:', result);
        } catch (error) {
            console.error('Error finding path:', error);
            alert('Failed to find path. Check the console for details.');
        }
    });


    async function drawPath(path, delay = 200) {
        // drawMap(mapData);
        drawSelection(startNode, 'green');
        drawSelection(endNode, 'red');
        
        // Enable smooth rendering for path
        ctx.imageSmoothingEnabled = true;
        ctx.imageSmoothingQuality = 'high';
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        ctx.miterLimit = 10;
        
        const pathWidth = 12;
        const shadowWidth = pathWidth + 2;

        const startNodeData = mapData.nodes.find(n => n.id === path[0]);
        let currentX = startNodeData.x;
        let currentY = startNodeData.y;

        for (let i = 1; i < path.length; i++) {
            const nodeData = mapData.nodes.find(n => n.id === path[i]);
            
            // Draw shadow first for depth
            ctx.beginPath();
            ctx.moveTo(currentX, currentY);
            ctx.lineTo(nodeData.x, nodeData.y);
            ctx.lineWidth = shadowWidth;
            ctx.strokeStyle = 'rgba(0, 0, 0, 0.4)';
            ctx.shadowBlur = 4;
            ctx.shadowColor = 'rgba(0, 0, 0, 0.3)';
            ctx.stroke();
            ctx.shadowBlur = 0;
            
            // Draw the main path
            ctx.beginPath();
            ctx.moveTo(currentX, currentY);
            ctx.lineTo(nodeData.x, nodeData.y);
            ctx.lineWidth = pathWidth;
            ctx.strokeStyle = '#3F84D9';
            ctx.stroke();
            
            currentX = nodeData.x;
            currentY = nodeData.y;

            // sleep for the specified delay, for animation effect 
            await new Promise(resolve => setTimeout(resolve, delay));
        }

        mapData.nodes.forEach(node => {
        ctx.drawImage(imgHouse, node.x - imgSize/2, node.y - imgSize/2, imgSize, imgSize);
    });
    }


    function displayResults(results) {
        // Add fade-in animation by temporarily hiding and showing
        resultsDiv.style.opacity = '0';
        resultsDiv.style.transform = 'translateY(10px)';
        
        setTimeout(() => {
            resultsDiv.innerHTML = `
                <h3>Path Details</h3>
                <p><strong>Distance:</strong> ${results.total_length} km</p>
                <p><strong>Time:</strong> ${results.total_time} min</p>
                <p><strong>Cost:</strong> ${results.total_money_cost} TL</p>
            `;
            resultsDiv.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            resultsDiv.style.opacity = '1';
            resultsDiv.style.transform = 'translateY(0)';
        }, 50);
    }


    resetPathButton.addEventListener('click', function() {
        // Reset the global variables
        startNode = null;
        endNode = null;
        console.log("Path has been reset. Start a new selection.");
        
        // Clear any old results displayed on the page
        resultsDiv.style.transition = 'opacity 0.3s ease';
        resultsDiv.style.opacity = '0';
        setTimeout(() => {
            resultsDiv.innerHTML = `
                <h3>Path Details</h3>
                <p><strong>Distance:</strong> <span id="distance">--</span></p>
                <p><strong>Time:</strong> <span id="time">--</span></p>
                <p><strong>Cost:</strong> <span id="cost">--</span></p>
            `;
            resultsDiv.style.opacity = '1';
        }, 300);

        // Redraw the map to remove the old path and highlights
        if (mapData) {
            drawMap(mapData);
        } else {
            // If the map data is gone, just clear the canvas completely
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        }
    }); 

};