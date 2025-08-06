document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('operacoes-formset-container');
    const addButton = document.getElementById('add-operacao-btn');
    const totalFormsInput = document.querySelector('input[name="operacoes-TOTAL_FORMS"]');
    
    const emptyFormHtml = `
        <div class="operacao-item new-form">
            <h3></h3>
            <input type="hidden" name="operacoes-__prefix__-DELETE" id="id_operacoes-__prefix__-DELETE"> 
            
            <div class="form-group">
                <label for="id_operacoes-__prefix__-nome_operacao">Qual o nome da operação a ser parametrizada?</label>
                <input type="text" name="operacoes-__prefix__-nome_operacao" id="id_operacoes-__prefix__-nome_operacao" placeholder="">
            </div>
            <div class="form-group">
                <label for="id_operacoes-__prefix__-valor_nivel_1">Qual o valor do operacional para o nível 1?</label>
                <input type="text" name="operacoes-__prefix__-valor_nivel_1" id="id_operacoes-__prefix__-valor_nivel_1" placeholder="">
            </div>
            <div class="form-group">
                <label for="id_operacoes-__prefix__-valor_nivel_2">Qual o valor do operacional para o nível 2?</label>
                <input type="text" name="operacoes-__prefix__-valor_nivel_2" id="id_operacoes-__prefix__-valor_nivel_2" placeholder="">
            </div>
            <div class="form-group">
                <label for="id_operacoes-__prefix__-valor_nivel_3">Qual o valor do operacional para o nível 3?</label>
                <input type="text" name="operacoes-__prefix__-valor_nivel_3" id="id_operacoes-__prefix__-valor_nivel_3" placeholder="">
            </div>
            <div class="form-group">
                <label for="id_operacoes-__prefix__-valor_nivel_4">Qual o valor do operacional para o nível 4?</label>
                <input type="text" name="operacoes-__prefix__-valor_nivel_4" id="id_operacoes-__prefix__-valor_nivel_4" placeholder="">
            </div>
            <div class="form-group">
                <label for="id_operacoes-__prefix__-valor_nivel_5">Qual o valor do operacional para o nível 5?</label>
                <input type="text" name="operacoes-__prefix__-valor_nivel_5" id="id_operacoes-__prefix__-valor_nivel_5" placeholder="">
            </div>
            <input type="hidden" name="operacoes-__prefix__-id" id="id_operacoes-__prefix__-id">
            <input type="hidden" name="operacoes-__prefix__-parametrizacao_bia" id="id_operacoes-__prefix__-parametrizacao_bia">
            <button type="button" class="btn-deletar">Remover esta operação</button>
        </div>
    `;

    function updateElementIndex(el, prefix, index) {
        el.querySelectorAll('input[id^="' + prefix + '"], input[name^="' + prefix + '"], label[for^="' + prefix + '"]').forEach(element => {
            const idRegex = new RegExp(`(${prefix}-(\\d+)-)`, 'g');
            const nameRegex = new RegExp(`(${prefix}-(\\d+)-)`, 'g');

            if (element.id) {
                element.id = element.id.replace(idRegex, `${prefix}-${index}-`);
            }
            if (element.name) {
                element.name = element.name.replace(nameRegex, `${prefix}-${index}-`);
            }
            if (element.tagName === 'LABEL' && element.htmlFor) {
                element.htmlFor = element.htmlFor.replace(idRegex, `${prefix}-${index}-`);
            }
        });

        const title = el.querySelector('h3');
        if (title) {
            title.textContent = `Operação #${index + 1}`;
        }
    }

    function addDeleteHandler(formItem, index) {
        const deleteButton = formItem.querySelector('.btn-deletar');
        // Pega o input hidden DELETE
        const deleteHiddenInput = formItem.querySelector('input[name$="-DELETE"][type="hidden"]'); 

        const handleRemoveButtonClick = function() {
            // Agora sim, tentamos marcar o hidden input se ele existir
            if (deleteHiddenInput) {
                deleteHiddenInput.value = 'on'; // Marca o campo DELETE como 'on'
                formItem.style.display = 'none'; // Esconde o formulário
            } else { 
                // Isso deve ser para formulários recém-adicionados que ainda não têm ID no BD
                formItem.remove(); // Remove o elemento do DOM
            }
            updateFormIndices();
        };

        if (index === 0) { // Primeira operação
            if (deleteButton) {
                deleteButton.disabled = true; // Desabilita o botão
                // Remova QUALQUER event listener anterior para o botão da primeira operação
                deleteButton.removeEventListener('click', handleRemoveButtonClick); 
            }
        } else { // Outras operações
            if (deleteButton) {
                deleteButton.disabled = false; // Garante que esteja habilitado
                // Remova listeners anteriores e adicione o novo
                deleteButton.removeEventListener('click', handleRemoveButtonClick);
                deleteButton.addEventListener('click', handleRemoveButtonClick);
            }
        }
    }

    function updateFormIndices() {
        const formItems = container.querySelectorAll('.operacao-item');
        let newIndex = 0;
        formItems.forEach((formItem, actualIndex) => { // Use actualIndex para a iteração real
            if (formItem.style.display !== 'none') {
                updateElementIndex(formItem, 'operacoes', newIndex);
                addDeleteHandler(formItem, newIndex); // Passa o índice lógico (newIndex)
                newIndex++;
            } else {
                // Se o formulário está oculto (marcado para exclusão),
                // certifique-se de que o campo DELETE hidden input esteja 'on'
                const deleteHiddenInput = formItem.querySelector('input[name$="-DELETE"][type="hidden"]');
                if (deleteHiddenInput) {
                    deleteHiddenInput.value = 'on';
                }
            }
        });
        totalFormsInput.value = newIndex;
    }

    addButton.addEventListener('click', function() {
        const currentTotalForms = parseInt(totalFormsInput.value); 
        
        const newFormDiv = document.createElement('div');
        newFormDiv.innerHTML = emptyFormHtml;

        const newFormItem = newFormDiv.firstElementChild;
        
        updateElementIndex(newFormItem, 'operacoes', currentTotalForms);
        
        container.appendChild(newFormItem);
        
        totalFormsInput.value = currentTotalForms + 1; 

        // Adiciona o handler para o novo formulário com o índice atualizado
        addDeleteHandler(newFormItem, currentTotalForms); 

        updateFormIndices(); 
    });

    updateFormIndices(); 
});