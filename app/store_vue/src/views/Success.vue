<template>
    <div class="page-success">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="has-text-success title"> Thank You for shopping with us!</h1>
                <p class="has-text-success">Your order will be processed within 24 hours</p>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: 'Success',
    mounted(){
        document.title = 'Success | Official Boots'
    }
    
}
</script>