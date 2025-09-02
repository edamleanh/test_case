import { Selector } from 'testcafe';
import { BASE_URL } from '../store';



fixture`Demo Login Test`
    .page`${BASE_URL}/accounts/login/`;

const usernameInput = Selector('#id_username');
const passwordInput = Selector('#id_password');
const logoImg = Selector('img[alt="DMOJ"][src="/static/icons/logo.svg"]');
const firstPostLink = Selector('a').withAttribute('href', '/post/1-first-post').withText('First Post');
const aceEditor = Selector('.ace_content');
const aceTextArea = Selector('textarea.ace_text-input'); 
const previewTab = Selector('a.item[data-tab="preview-tab-body"]').withText('Preview');
const editButton = Selector('a.edit-link[title="Edit"][href="/comments/9/edit"]');
const editorTextArea = Selector('#id_edit');
const postButton = Selector('input[type="submit"]').withAttribute('value', 'Post!').withAttribute('class', 'button');
const editPostButton = Selector('form#comment-edit input[type="submit"][value="Post!"]');
const editSuccessMessage = Selector('.comment-body p').withText('Edit comment');
test('User can log in with valid credentials', async t => {

    await t
        .typeText(usernameInput, 'admin')
        .typeText(passwordInput, 'Ducanh12a1@!')
        .pressKey('enter')
        .click(logoImg)
        .click(firstPostLink)
        .click(editButton);
    await t
        .expect(editorTextArea.exists).ok('Editor textarea is visible')
        .click(editorTextArea)
        .selectText(editorTextArea)
        .pressKey('delete')
        .click(editPostButton)
        
});

