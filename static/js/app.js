(function () {
  'use strict';

  // ---------- Element references ----------
  const chatBox = document.getElementById('chat-box');
  const chatEmptyState = document.getElementById('chat-empty-state');
  const userInput = document.getElementById('user-question-input');
  const sendBtn = document.getElementById('send-btn');

  const fileInput = document.getElementById('file-input');
  const fileDropZone = document.getElementById('file-drop-zone');
  const fileDropText = document.getElementById('file-drop-text');
  const sourceTypeSelect = document.getElementById('source-type-select');
  const uploadBtn = document.getElementById('upload-btn');
  const uploadBtnText = document.getElementById('upload-btn-text');
  const uploadStatus = document.getElementById('upload-status');

  // ---------- Helpers ----------
  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  function scrollChatToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function removeEmptyState() {
    if (chatEmptyState && chatEmptyState.parentNode) {
      chatEmptyState.remove();
    }
  }

  function appendUserMessage(text) {
    removeEmptyState();
    const row = document.createElement('div');
    row.className = 'msg-row user';
    row.innerHTML = `
      <div class="bubble user-bubble">
        <div class="bubble-meta">You</div>
        ${escapeHtml(text)}
      </div>
    `;
    chatBox.appendChild(row);
    scrollChatToBottom();
  }

  function appendAiMessage(text) {
    removeEmptyState();
    const row = document.createElement('div');
    row.className = 'msg-row ai';
    row.innerHTML = `
      <div class="ai-avatar"><i class="bi bi-robot"></i></div>
      <div class="bubble ai-bubble">
        <div class="bubble-meta">Assistant</div>
        ${escapeHtml(text)}
      </div>
    `;
    chatBox.appendChild(row);
    scrollChatToBottom();
  }

  function appendTypingIndicator() {
    removeEmptyState();
    const row = document.createElement('div');
    row.className = 'msg-row ai';
    row.id = 'typing-row';
    row.innerHTML = `
      <div class="ai-avatar"><i class="bi bi-robot"></i></div>
      <div class="bubble ai-bubble">
        <div class="typing-indicator"><span></span><span></span><span></span></div>
      </div>
    `;
    chatBox.appendChild(row);
    scrollChatToBottom();
    return row;
  }

  function removeTypingIndicator() {
    const row = document.getElementById('typing-row');
    if (row) row.remove();
  }

  // ---------- Chat logic ----------
  async function sendMessage() {
    const question = userInput.value.trim();
    if (!question) return;

    appendUserMessage(question);
    userInput.value = '';
    userInput.focus();

    sendBtn.disabled = true;
    const typingRow = appendTypingIndicator();

    try {
      const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: question })
      });

      removeTypingIndicator();

      if (!response.ok) {
        let errMsg = 'Something went wrong while reaching the assistant.';
        try {
          const errData = await response.json();
          if (errData && errData.error) errMsg = errData.error;
        } catch (_) { /* ignore parse errors */ }
        appendAiMessage(`⚠️ ${errMsg}`);
        return;
      }

      const data = await response.json();
      const answer = (data && data.answer) ? data.answer : 'I could not find an answer to that. Could you rephrase your question?';
      appendAiMessage(answer);

    } catch (err) {
      removeTypingIndicator();
      appendAiMessage('⚠️ Could not connect to the server. Please check your connection and try again.');
      console.error('Chat request failed:', err);
    } finally {
      sendBtn.disabled = false;
    }
  }

  sendBtn.addEventListener('click', sendMessage);

  userInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  // ---------- Upload logic ----------
  fileInput.addEventListener('change', function () {
    if (fileInput.files && fileInput.files.length > 0) {
      const file = fileInput.files[0];
      fileDropText.textContent = file.name;
      fileDropZone.classList.add('has-file');
    } else {
      fileDropText.textContent = 'Click to choose a file';
      fileDropZone.classList.remove('has-file');
    }
  });

  function showUploadStatus(message, isSuccess) {
    const alertClass = isSuccess ? 'alert-success' : 'alert-danger';
    const icon = isSuccess ? 'bi-check-circle-fill' : 'bi-exclamation-triangle-fill';
    uploadStatus.innerHTML = `
      <div class="alert ${alertClass} mb-0" role="alert">
        <i class="bi ${icon}"></i>
        <span>${escapeHtml(message)}</span>
      </div>
    `;
  }

  function clearUploadStatus() {
    uploadStatus.innerHTML = '';
  }

  async function uploadFile() {
    const file = fileInput.files && fileInput.files[0];
    const sourceType = sourceTypeSelect.value;

    if (!file) {
      showUploadStatus('Please choose a PDF or CSV file before uploading.', false);
      return;
    }

    const formData = new FormData();
    formData.append('file-input', file);
    formData.append('source_type', sourceType);

    uploadBtn.disabled = true;
    uploadBtnText.textContent = 'Indexing...';
    clearUploadStatus();

    try {
      const response = await fetch('/upload', {
        method: 'POST',
        body: formData
      });

      const data = await response.json().catch(() => ({}));

      if (response.ok) {
        const successMsg = data.message || 'File uploaded and indexed successfully.';
        showUploadStatus(successMsg, true);
        // Reset file input on success
        fileInput.value = '';
        fileDropText.textContent = 'Click to choose a file';
        fileDropZone.classList.remove('has-file');
      } else {
        const errorMsg = data.error || 'Upload failed. Please try again.';
        showUploadStatus(errorMsg, false);
      }
    } catch (err) {
      showUploadStatus('Could not connect to the server. Please try again.', false);
      console.error('Upload request failed:', err);
    } finally {
      uploadBtn.disabled = false;
      uploadBtnText.textContent = 'Upload & Index';
    }
  }

  uploadBtn.addEventListener('click', uploadFile);

})();