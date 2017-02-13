define(require => {
    'use strict'

    const $ = require('jquery')
    const Jupyter = require('base/js/namespace')

    const getConfig = () => {
        const config = Jupyter.notebook.metadata.displacy || {}

        return {
            distance: config.distance || 200,
            offsetX: config.offsetX || 50,
            arrowSpacing: config.arrowSpacing || 20,
            arrowWidth: config.arrowWidth || 10,
            arrowStroke: config.arrowStorke || 2,
            wordSpacing: config.wordSpacing || 75,
            font: config.font || 'inherit',
            color: config.color || '#000000',
            bg: config.bg || '#ffffff'
        }
    }

    const render = (parse, id) => {
        const opts = getConfig()
        const levels = [...new Set(parse.arcs.map(({ end, start }) => end - start).sort((a, b) => a - b))]
        const highestLevel = levels.indexOf(levels.slice(-1)[0]) + 1
        const offsetY = opts.distance / 2 * highestLevel
        const width = opts.offsetX + parse.words.length * opts.distance
        const height = offsetY + 3 * opts.wordSpacing

        return `
            <svg id="displacy-${id}" class="displacy" width="${width}"
                height="${height}" viewBox="0 0 ${width} ${height}" preserveAspectRatio="xMinYMax meet"
                style="color: ${opts.color}; background: ${opts.bg}; font-family: ${opts.font}">

                ${parse.words.map(({ text, tag }, i) => `
                    <text class="displacy-token" fill="currentColor"
                        data-tag="${tag}" text-anchor="middle"
                        y="${offsetY + opts.wordSpacing}">

                        <tspan class="displacy-word" fill="currentColor"
                            x="${opts.offsetX + i * opts.distance}">
                            ${text}
                        </tspan>

                        <tspan class="displacy-tag" dy="2em" fill="currentColor"
                            x="${opts.offsetX + i * opts.distance}">
                            ${tag}
                        </tspan>
                    </text>
                `).join('')}

                ${parse.arcs.map(({ label, end, start, dir }, i) => {
                    const level = levels.indexOf(end - start) + 1
                    const startX = opts.offsetX + start * opts.distance + opts.arrowSpacing * (highestLevel - level) / 4
                    const startY = offsetY
                    const endpoint = opts.offsetX + (end - start) * opts.distance + start * opts.distance - opts.arrowSpacing * (highestLevel - level) / 4

                    let curve = offsetY - level * opts.distance / 2
                    if(curve == 0 && levels.length > 5) curve = -opts.distance

                    return `
                        <g class="displacy-arrow" data-dir="${dir}"
                            data-label="${label}">

                            <path class="displacy-arc" id="arrow-${id}-${i}"
                            d="M${startX},${startY} C${startX},${curve} ${endpoint},${curve} ${endpoint},${startY}"
                            stroke-width="${opts.arrowStroke}px" fill="none" stroke="currentColor" data-dir="${dir}"
                            data-label="${label}"/>

                            <text dy="1em">
                                <textPath xlink:href="#arrow-${id}-${i}"
                                    class="displacy-label" startOffset="50%"
                                    fill="currentColor" text-anchor="middle"
                                    data-label="${label}" data-dir="${dir}">
                                    ${label}
                                </textPath>
                            </text>

                            <path class="displacy-arrowhead" fill="currentColor"
                                d="M${(dir == 'left') ? startX : endpoint},${startY + 2} L${(dir == 'left') ? startX - opts.arrowWidth + 2 : endpoint + opts.arrowWidth - 2},${startY - opts.arrowWidth} ${(dir == 'left') ? startX + opts.arrowWidth - 2 : endpoint - opts.arrowWidth + 2},${startY - opts.arrowWidth}"
                                data-label="${label}" data-dir="${dir}"/>
                        </g>
                `}).join('')}
            </svg>
        `
    }

    const removeWS = (text) => {
        return text.replace(/([^"]+)|("(?:[^"\\]|\\.)+")/g, ($0, $1, $2) => {
            if ($1) return $1.replace(/\s|\u200B/g, '')
            else return $2
        })
    }

    const displacy = () => {
        const cell = Jupyter.notebook.get_selected_cell()
        const content = removeWS(cell.code_mirror.display.wrapper.textContent)
        const wrapper = `#wrapper-${cell.cell_id}`

        if (!$(wrapper).length) $(cell.element).after(`
            <div id="wrapper-${cell.cell_id}"
                style="max-width: 100%; overflow-x: scroll; margin-top: 10px;">
            </div>
        `)

        try {
            const parse = render(JSON.parse(content), cell.cell_id)
            $(wrapper).html(parse)
        }

        catch(error) {
            $(wrapper).html(`
                <div style="border: 3px solid red; padding: 10px;">
                    <strong>Error:</strong> Parse seems to be invalid JSON. <code>${error}</code>
                </div>
            `)
        }
    }

    const load_ipython_extension = () => {
        Jupyter.toolbar.add_buttons_group([{
            id : 'displacy',
            label : 'Render with displaCy',
            icon : 'fa-magic',
            callback : displacy
        }])
    }

    return ({ load_ipython_extension })
})
