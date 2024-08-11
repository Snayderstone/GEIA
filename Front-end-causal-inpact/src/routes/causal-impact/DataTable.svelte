<!-- Table.svelte -->
<script>
    export let data = [];
</script>

{#if data.length > 0}
    <div class="overflow-x-auto">
        <table class="min-w-full bg-white border border-gray-300">
            <thead>
                <tr>
                    {#each Object.keys(data[0]) as key}
                        <th class="px-4 py-2 border">{key}</th>
                    {/each}
                </tr>
            </thead>
            <tbody>
                {#each data.slice(0, 15) as row}
                    <tr class="odd:bg-gray-100 even:bg-white">
                        {#each Object.values(row) as value}
                            <td class="px-4 py-2 border">{value}</td>
                        {/each}
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>
{/if}

<style>
    
</style>