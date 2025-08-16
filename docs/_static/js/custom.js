// Custom JavaScript for greeting_toolkit documentation

document.addEventListener('DOMContentLoaded', function() {
    // Add copy buttons to code blocks
    document.querySelectorAll('div[class^="highlight"]').forEach(function(codeBlock) {
        // Create the copy button
        var button = document.createElement('button');
        button.className = 'copy-button';
        button.textContent = 'Copy';

        // Add the button to the code block
        codeBlock.appendChild(button);

        // Add click event listener to the button
        button.addEventListener('click', function() {
            // Find the <code> element within the code block
            var code = codeBlock.querySelector('code');
            var text = code.innerText;

            // Create a temporary textarea element to copy the text
            var textarea = document.createElement('textarea');
            textarea.value = text;
            textarea.setAttribute('readonly', '');
            textarea.style.position = 'absolute';
            textarea.style.left = '-9999px';
            document.body.appendChild(textarea);

            // Select and copy the text
            textarea.select();
            document.execCommand('copy');

            // Remove the textarea
            document.body.removeChild(textarea);

            // Change the button text to indicate success
            button.textContent = 'Copied!';

            // Reset the button text after a delay
            setTimeout(function() {
                button.textContent = 'Copy';
            }, 2000);
        });
    });

    // Add styles for the copy button
    var style = document.createElement('style');
    style.textContent = `
        .copy-button {
            position: absolute;
            top: 5px;
            right: 5px;
            background-color: #2980b9;
            color: white;
            border: none;
            border-radius: 3px;
            padding: 5px 10px;
            font-size: 12px;
            cursor: pointer;
            opacity: 0;
            transition: opacity 0.2s;
        }
        div[class^="highlight"] {
            position: relative;
        }
        div[class^="highlight"]:hover .copy-button {
            opacity: 1;
        }
        .copy-button:hover {
            background-color: #3498db;
        }
    `;
    document.head.appendChild(style);

    // Add anchor links to headings
    document.querySelectorAll('h2, h3, h4, h5, h6').forEach(function(heading) {
        if (heading.id) {
            // Create the anchor link
            var link = document.createElement('a');
            link.className = 'headerlink';
            link.href = '#' + heading.id;
            link.title = 'Permalink to this heading';
            link.innerHTML = '¶';

            // Add the link to the heading
            heading.appendChild(link);
        }
    });

    // Add example collapsers
    document.querySelectorAll('.admonition.example').forEach(function(example) {
        var title = example.querySelector('.admonition-title');
        if (title) {
            title.style.cursor = 'pointer';

            // Create a toggle button
            var toggle = document.createElement('span');
            toggle.className = 'example-toggle';
            toggle.innerHTML = '[-]';
            toggle.style.float = 'right';
            toggle.style.marginRight = '5px';
            title.appendChild(toggle);

            // Add click event listener to the title
            title.addEventListener('click', function() {
                // Find the content of the example
                var content = example.querySelectorAll(':scope > *:not(.admonition-title)');

                // Toggle the visibility of the content
                var isVisible = content[0].style.display !== 'none';
                content.forEach(function(element) {
                    element.style.display = isVisible ? 'none' : '';
                });

                // Update the toggle button
                toggle.innerHTML = isVisible ? '[+]' : '[-]';
            });
        }
    });
});
