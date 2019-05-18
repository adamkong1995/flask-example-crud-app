// Add keywords
document.querySelector('#add_btn').addEventListener('click', async () => {
    const data = document.querySelector('#news_keywords').value;
    const im = document.querySelector('#im').value;

    if(data) {
         const res = await fetch('/add_keywords', {
            method: 'post',
            headers: {
                'Accept': 'application/json',
                'Content-type': 'application/json'
            },
            body: JSON.stringify({ keywords:data, im:im })
        });

        document.querySelector('#news_keywords').value = ''
        loadKeywords();
    };
});

// Load keywords list
const loadKeywords = async () => {
    const im = document.querySelector('#im').value;

    const res = await fetch('/load_keywords', { 
        method: 'post',
        headers: {
            'Accept': 'application/json',
            'Content-type': 'application/json'
        },
        body: JSON.stringify({ im })
    });

    const json = await res.json();
    const data = await JSON.parse(json)

    const list = document.querySelector('#keywords_list')
    list.innerHTML = ''

    for(record of data){
        list.insertAdjacentHTML('beforeend', `
            <div class='row mt-2'>
                <div class="col-lg-4 offset-lg-4">
                    ${record.keyword}
                </div>
                <div class="col-6 col-lg-2 mt-2 mt-lg-0">
                    <button class="btn btn-danger btn-sm btn-block no-print delete_btn" id="${record.keyword_id}">Delete</button>
                </div>
            </div>
        `)
    }

    init_delete_handlers();
};

$("#im").on('changed.bs.select', () => {
    loadKeywords(this.value);
});

// Delete Keywords
const init_delete_handlers = () => {
    const buttons = document.querySelectorAll('.delete_btn');
    Array.from(buttons).forEach(button => {
        button.addEventListener('click', async e => {
            const res = await fetch('delete_keywords', {
                method: 'post',
                headers: {
                    'Accept': 'application/json',
                    'Content-type': 'application/json'
                },
                body: JSON.stringify({ id: e.target.id })
            });

            loadKeywords();
        });
    });
};

// Load news keywords query and show query modal
document.querySelector('#get_query').addEventListener('click', async ()=>{
    const im = document.querySelector('#im').value;

    const res = await fetch('/load_keywords', {
        method: 'post',
        headers: {
            'Accept': 'application/json',
            'Content-type': 'application/json'
        },
        body: JSON.stringify({ im })
    });

    const json = await res.json();
    const data = await JSON.parse(json);

    let query = '';

    for(record of data){
        if (query === ''){
            query = record.keyword
        } else {
            query = `${query} or ${record.keyword}`
        };
    };

    document.querySelector('#query').innerHTML = query;

    $('#query_modal').modal();
});
